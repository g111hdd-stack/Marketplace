import os
import shutil
import zipfile
import asyncio
import requests
import warnings
import tempfile

import logging
import nest_asyncio
import pandas as pd
from pathlib import Path

from collections import defaultdict
from datetime import timedelta, date, datetime
from sqlalchemy.exc import OperationalError

from ya_sdk.ya_api import YandexApi
from database import YaDbConnection
from data_classes import DataYaReportConsolidated

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

warnings.simplefilter(action='ignore', category=UserWarning)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def sanitize_xlsx_file(file_path: str) -> str | None:
    """
    Удаляет styles.xml из xlsx-файла, чтобы обойти ошибки openpyxl.

    Args:
        file_path (str): Путь к исходному .xlsx файлу.

    Returns:
        str | None: Путь к очищенному файлу или None, если не удалось.
    """
    try:
        # Создаем временную папку для распаковки
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Путь к файлу стилей
        styles_path = Path(temp_dir) / "xl" / "styles.xml"
        if styles_path.exists():
            styles_path.unlink()  # Удаляем styles.xml

        # Собираем очищенный файл
        with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
            for foldername, subfolders, filenames in os.walk(temp_dir):
                for filename in filenames:
                    file_full_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_full_path, temp_dir)
                    new_zip.write(file_full_path, arcname)

        shutil.rmtree(temp_dir)
        return file_path

    except Exception as e:
        raise Exception(f"Ошибка при очистке файла: {e}")


def download_file(url, file_name) -> str or None:
    try:
        response = requests.get(url)
        response.raise_for_status()

        save_path = os.path.join(PROJECT_ROOT, 'templates', 'yandex_report_consolidated', f'{file_name}.xlsx')

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as file:
            file.write(response.content)

        sanitize_xlsx_file(file_path=save_path)

        logger.info(f'Файл сохранен по пути: {save_path}')
        return save_path

    except requests.exceptions.RequestException as e:
        logger.error(f'Ошибка при скачивании файла: {e}')
        return None
    except Exception as e:
        logger.error(f'Неожиданная ошибка: {e}')
        return None


def convert_id(number):
    if number is not None:
        number = str(number).split('.')[0]
    return number


async def report_generate(client_id: str, api_key: str, date_now: date) -> str or None:
    date_from = date_now - timedelta(days=1)
    date_to = date_now - timedelta(days=1)

    report_id = None
    link_report = None
    substatus = {'NO_DATA': 'Для такого отчета нет данных.',
                 'TOO_LARGE': 'Отчет превысил допустимый размер — укажите меньший период времени '
                              'или уточните условия запроса.',
                 'RESOURCE_NOT_FOUND': 'Для такого отчета не удалось найти часть сущностей.'}
    api_user = YandexApi(api_key=api_key)
    answer = await api_user.get_reports_boost_consolidated_generate(business_id=int(client_id),
                                                                    date_from=date_from.isoformat(),
                                                                    date_to=date_to.isoformat())
    if answer:
        if answer.result:
            report_id = answer.result.reportId
            logger.info(f"Запрос отправлен: {report_id}")

    if report_id is not None:
        retry = 3
        while True:
            await asyncio.sleep(10)
            answer_report_info = await api_user.get_reports_info(report_id=report_id)
            if answer_report_info:
                if answer_report_info.result:
                    if answer_report_info.result.status == 'DONE':
                        link_report = answer_report_info.result.file
                        if link_report is not None:
                            logger.info(f"Отчёт: {link_report}")
                        else:
                            logger.info(f"{substatus.get(answer_report_info.result.subStatus, None)}")
                        break
                    elif answer_report_info.result.status == 'FAILED':
                        logger.error(f"Ошибка формирования отчёта: FAILED")
                        break
                else:
                    retry -= 1
                    if not retry:
                        logger.error(f"Ошибка формирования отчёта: пустой result")
                        break
            else:
                retry -= 1
                if not retry:
                    logger.error(f"Ошибка формирования отчёта: пустой answer_report_info")
                    break
    else:
        logger.error(f"Не получилось отправить запрос")

    if link_report is not None:
        path_file = download_file(url=link_report, file_name=f'{client_id}_{date_to}')
        return path_file
    else:
        return None


async def add_yandex_report_entry(path_file: str, client_id: str, from_date: date) -> list[DataYaReportConsolidated]:
    headers_dict = {'vendor_code': {'Ваш SKU': None},
                    'name_product': {'Название товара': None},
                    'boost_shows': {'Показы товара с бустом, шт.': None},
                    'total_shows': {'Все показы товара, шт.': None},
                    'boost_clicks': {'Клики по товару с бустом, шт.': None},
                    'total_clicks': {'Все клики по товару, шт.': None},
                    'boost_add_to_card': {'Добавления в корзину товаров с бустом, шт.': None},
                    'total_add_to_card': {'Все добавления товаров в корзину, шт.': None},
                    'boost_orders_count': {'Заказанные товары с бустом, шт.': None},
                    'total_orders_count': {'Все заказанные товары, шт.': None},
                    'boost_orders_delivered_count': {'Доставленные товары с бустом, шт.': None},
                    'total_orders_delivered_count': {'Всего доставлено товаров, шт.': None},
                    'cost': {'Расходы на буст, ₽': None},
                    'bonus_cost': {'Списано бонусов': None},
                    'average_cost': {'Средняя стоимость буста, ₽': None},
                    'boost_cost_ratio_revenue': {'Доля расходов на буст от выручки с бустом, %': None},
                    'boost_orders_delivered_sum': {'Выручка с бустом, ₽': None},
                    'total_orders_delivered_sum': {'Вся выручка, ₽': None},
                    'boost_revenue_ratio_total': {'Доля выручки с бустом от всей выручки, %': None},
                    'advert_id': {'ID кампаний': None},
                    'name_advert': {'Названия кампаний': None}}
    headers = [key for val in headers_dict.values() for key in val.keys()]

    name_sheets = ['Сводный отчет']

    try:
        excel_file = pd.ExcelFile(path_file)
        logger.info(f'Файл {path_file} прочитан успешно.')

        sheet_names = excel_file.sheet_names

        result_data = []

        for sheet in name_sheets:
            if sheet in sheet_names:
                df = pd.read_excel(path_file, sheet_name=sheet, header=None)

                header_row = 0
                for i, row in df.iterrows():
                    if any(cell in headers for cell in row if pd.notna(cell)):
                        header_row = i
                        break

                df = pd.read_excel(path_file, sheet_name=sheet, header=header_row)
                df = df.fillna('')

                for idx, row in df.iterrows():
                    try:
                        row_data = {}
                        for metric, value in headers_dict.items():
                            row_data[metric] = {}
                            for header in value.keys():
                                if header in df.columns:
                                    row_data[metric][header] = row[header]

                        vendor_code = next((v for v in row_data.get('vendor_code', {}).values() if v is not None), None)
                        name_product = next((v for v in row_data.get('name_product', {}).values() if v is not None), None)
                        boost_shows = next((v for v in row_data.get('boost_shows', {}).values() if v is not None), None)
                        total_shows = next((v for v in row_data.get('total_shows', {}).values() if v is not None), None)
                        boost_clicks = next((v for v in row_data.get('boost_clicks', {}).values() if v is not None), None)
                        total_clicks = next((v for v in row_data.get('total_clicks', {}).values() if v is not None), None)
                        boost_add_to_card = next((v for v in row_data.get('boost_add_to_card', {}).values() if v is not None), None)
                        total_add_to_card = next((v for v in row_data.get('total_add_to_card', {}).values() if v is not None), None)
                        boost_orders_count = next((v for v in row_data.get('boost_orders_count', {}).values() if v is not None), None)
                        total_orders_count = next((v for v in row_data.get('total_orders_count', {}).values() if v is not None), None)
                        boost_orders_delivered_count = next((v for v in row_data.get('boost_orders_delivered_count', {}).values() if v is not None), None)
                        total_orders_delivered_count = next((v for v in row_data.get('total_orders_delivered_count', {}).values() if v is not None), None)
                        cost = next((v for v in row_data.get('cost', {}).values() if v is not None), None)
                        bonus_cost = next((v for v in row_data.get('bonus_cost', {}).values() if v is not None), None)
                        average_cost = next((v for v in row_data.get('average_cost', {}).values() if v is not None), None)
                        boost_cost_ratio_revenue = next((v for v in row_data.get('boost_cost_ratio_revenue', {}).values() if v is not None), None)
                        boost_orders_delivered_sum = next((v for v in row_data.get('boost_orders_delivered_sum', {}).values() if v is not None), None)
                        total_orders_delivered_sum = next((v for v in row_data.get('total_orders_delivered_sum', {}).values() if v is not None), None)
                        boost_revenue_ratio_total = next((v for v in row_data.get('boost_revenue_ratio_total', {}).values() if v is not None), None)
                        advert_id = next((v for v in row_data.get('advert_id', {}).values() if v is not None), None)
                        name_advert = next((v for v in row_data.get('name_advert', {}).values() if v is not None), None)

                        boost_shows = int(boost_shows)
                        total_shows = int(total_shows)
                        boost_clicks = int(boost_clicks)
                        total_clicks = int(total_clicks)
                        boost_add_to_card = int(boost_add_to_card)
                        total_add_to_card = int(total_add_to_card)
                        boost_orders_count = int(boost_orders_count)
                        total_orders_count = int(total_orders_count)
                        boost_orders_delivered_count = int(boost_orders_delivered_count)
                        total_orders_delivered_count = int(total_orders_delivered_count)
                        cost = round(float(cost), 2)
                        bonus_cost = round(float(bonus_cost), 2)
                        average_cost = round(float(average_cost), 2)
                        boost_cost_ratio_revenue = round(float(boost_cost_ratio_revenue), 2)
                        boost_orders_delivered_sum = round(float(boost_orders_delivered_sum), 2)
                        total_orders_delivered_sum = round(float(total_orders_delivered_sum), 2)
                        boost_revenue_ratio_total = round(float(boost_revenue_ratio_total), 2)

                        entry = DataYaReportConsolidated(client_id=client_id,
                                                         date=from_date,
                                                         vendor_code=vendor_code,
                                                         name_product=name_product,
                                                         boost_shows=boost_shows,
                                                         total_shows=total_shows,
                                                         boost_clicks=boost_clicks,
                                                         total_clicks=total_clicks,
                                                         boost_add_to_card=boost_add_to_card,
                                                         total_add_to_card=total_add_to_card,
                                                         boost_orders_count=boost_orders_count,
                                                         total_orders_count=total_orders_count,
                                                         boost_orders_delivered_count=boost_orders_delivered_count,
                                                         total_orders_delivered_count=total_orders_delivered_count,
                                                         cost=cost,
                                                         bonus_cost=bonus_cost,
                                                         average_cost=average_cost,
                                                         boost_cost_ratio_revenue=boost_cost_ratio_revenue,
                                                         boost_orders_delivered_sum=boost_orders_delivered_sum,
                                                         total_orders_delivered_sum=total_orders_delivered_sum,
                                                         boost_revenue_ratio_total=boost_revenue_ratio_total,
                                                         advert_id=advert_id,
                                                         name_advert=name_advert)
                        result_data.append(entry)
                    except Exception as e:
                        logger.error(f'Ошибка при чтении листа {sheet} строки {idx}: {e}')
            else:
                logger.error(f'Лист "{sheet}" не найден в файле.')

        aggregate = defaultdict(list)
        for stat in result_data:
            key = (
                stat.client_id,
                stat.date,
                stat.vendor_code,
                stat.name_product,
                stat.advert_id,
                stat.name_advert
            )
            aggregate[key].append(stat)

        result_data = []
        for key, group in aggregate.items():
            client_id, field_date, vendor_code, name_product, advert_id, name_advert = key

            # Суммируем простые числовые поля
            boost_shows = sum(x.boost_shows for x in group)
            total_shows = sum(x.total_shows for x in group)
            boost_clicks = sum(x.boost_clicks for x in group)
            total_clicks = sum(x.total_clicks for x in group)
            boost_add_to_card = sum(x.boost_add_to_card for x in group)
            total_add_to_card = sum(x.total_add_to_card for x in group)
            boost_orders_count = sum(x.boost_orders_count for x in group)
            total_orders_count = sum(x.total_orders_count for x in group)
            boost_orders_delivered_count = sum(x.boost_orders_delivered_count for x in group)
            total_orders_delivered_count = sum(x.total_orders_delivered_count for x in group)
            cost = sum(x.cost for x in group)
            bonus_cost = sum(x.bonus_cost for x in group)
            boost_orders_delivered_sum = sum(x.boost_orders_delivered_sum for x in group)
            total_orders_delivered_sum = sum(x.total_orders_delivered_sum for x in group)

            # Средняя стоимость буста (взвешенная по заказам)
            average_cost = (
                cost / boost_orders_count if boost_orders_count else 0
            )

            # Доля расходов от выручки
            boost_cost_ratio_revenue = (
                cost / boost_orders_delivered_sum * 100 if boost_orders_delivered_sum else 0
            )

            # Доля выручки с бустом от всей выручки
            revenue_ratio_boost_total = (
                boost_orders_delivered_sum / total_orders_delivered_sum * 100 if total_orders_delivered_sum else 0
            )

            result_data.append(DataYaReportConsolidated(
                client_id=client_id,
                date=field_date,
                vendor_code=vendor_code,
                name_product=name_product,
                boost_shows=boost_shows,
                total_shows=total_shows,
                boost_clicks=boost_clicks,
                total_clicks=total_clicks,
                boost_add_to_card=boost_add_to_card,
                total_add_to_card=total_add_to_card,
                boost_orders_count=boost_orders_count,
                total_orders_count=total_orders_count,
                boost_orders_delivered_count=boost_orders_delivered_count,
                total_orders_delivered_count=total_orders_delivered_count,
                cost=round(cost, 2),
                bonus_cost=round(bonus_cost, 2),
                average_cost=round(average_cost, 2),
                boost_cost_ratio_revenue=round(boost_cost_ratio_revenue, 2),
                boost_orders_delivered_sum=round(boost_orders_delivered_sum, 2),
                total_orders_delivered_sum=round(total_orders_delivered_sum, 2),
                boost_revenue_ratio_total=round(revenue_ratio_boost_total, 2),
                advert_id=advert_id,
                name_advert=name_advert
            ))

        logger.info(f'Количество записей: {len(result_data)}')
        return result_data
    except Exception as e:
        logger.error(f'Ошибка при чтении файла {path_file}: {e}')


async def main_yandex_report(retries: int = 6) -> None:
    """
        Основная функция для обновления записей в базе данных.

        Получает список клиентов из базы данных,
        затем для каждого клиента добавляет записи за вчерашний день в таблицу `ya_report`.
    """
    try:
        db_conn = YaDbConnection()
        db_conn.start_db()

        clients = db_conn.get_clients(marketplace='Yandex')

        date_now = date.today()

        logger.info(f"За дату {date_now - timedelta(days=1)}")
        for client in clients:
            logger.info(f"Добавление в базу данных компании '{client.name_company}'")
            path_file = await report_generate(client_id=client.client_id,
                                              api_key=client.api_key,
                                              date_now=date_now)
            if path_file is not None:
                list_reports = await add_yandex_report_entry(path_file=path_file,
                                                             client_id=client.client_id,
                                                             from_date=date_now - timedelta(days=1))
                db_conn.add_ya_report_consolidated(list_reports=list_reports)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_yandex_report(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_yandex_report())
    loop.stop()
