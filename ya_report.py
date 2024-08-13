import asyncio
import os
import requests
import warnings

import nest_asyncio
import logging
import pandas as pd

from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import OperationalError

from data_classes import DataYaReport, DataYaCampaigns
from ya_sdk.ya_api import YandexApi
from database import YaDbConnection

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

warnings.simplefilter(action='ignore', category=UserWarning)


def download_file(url, file_name) -> str or None:
    try:
        response = requests.get(url)
        response.raise_for_status()

        save_path = os.path.join('templates', 'yandex_report', f'{file_name}.xlsx')

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as file:
            file.write(response.content)
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


async def get_campaign_ids(api_key: str) -> list[DataYaCampaigns]:
    list_campaigns = []
    api_user = YandexApi(api_key=api_key)
    answer = await api_user.get_campaigns()
    if answer:
        for campaign in answer.campaigns:
            list_campaigns.append(DataYaCampaigns(client_id=str(campaign.business.field_id),
                                                  campaign_id=str(campaign.field_id),
                                                  name=campaign.domain,
                                                  placement_type=campaign.placementType))
    return list_campaigns


async def report_generate(client_id: str, api_key: str, campaign_id: str, from_date: str) -> str or None:
    report_id = None
    link_report = None
    substatus = {'NO_DATA': 'Для такого отчета нет данных.',
                 'TOO_LARGE': 'Отчет превысил допустимый размер — укажите меньший период времени '
                              'или уточните условия запроса.',
                 'RESOURCE_NOT_FOUND': 'Для такого отчета не удалось найти часть сущностей.'}
    api_user = YandexApi(api_key=api_key)
    answer = await api_user.get_reports_united_marketplace_services_generate(business_id=int(client_id),
                                                                             campaign_ids=[int(campaign_id)],
                                                                             date_from=from_date,
                                                                             date_to=from_date)
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
        path_file = download_file(url=link_report, file_name=f'{campaign_id}_{from_date}')
        return path_file
    else:
        return None


async def add_yandex_report_entry(path_file: str) -> list[DataYaReport]:
    headers = {'ID бизнес-аккаунта': None,
               'Номер заказа': None,
               'Номер заявки на утилизацию': None,
               'Ваш SKU': None,
               'Услуга': None,
               'Дата оказания услуги': None,
               'Дата и время оказания услуги': None,
               'Стоимость услуги (гр.46=гр. 34-гр.36+гр.41+гр.43-гр.44-гр.45), ₽': None,
               'Стоимость услуги, ₽': None,
               'Стоимость услуги': None,
               'Постоплата, ₽': None,
               'Номер заявки на Маркете': None,
               'Номер кампании': None,
               'Стоимость платного хранения, ₽': None}
    name_sheets = ['Размещение товаров на витрине',
                   'Обработка заказов в СЦ или ПВЗ',
                   'Обработка заказов на складе',
                   'Организация утилизации',
                   'Доставка покупателю',
                   'Экспресс-доставка покупателю',
                   'Доставка из-за рубежа',
                   'Вывоз со склада, СЦ, ПВЗ',
                   'Буст продаж, оплата за продажи',
                   'Буст продаж, оплата за показы',
                   'Программа лояльности и отзывы',
                   'Полки',
                   'Перевод платежа',
                   'Приём платежа',
                   'Хранение невыкупов и возвратов']
    campaign_id = path_file.split('\\')[-1].split('_')[0]

    try:
        excel_file = pd.ExcelFile(path_file)
        logger.info(f'Файл {path_file} прочитан успешно.')

        sheet_names = excel_file.sheet_names
        for s in sheet_names:
            if 'Платное хранение' in s:
                name_sheets.append(s)
        result_data = []

        for sheet in name_sheets:
            if sheet in sheet_names:
                df = pd.read_excel(path_file, sheet_name=sheet, header=None)

                header_row = 0
                for i, row in df.iterrows():
                    if any(cell in headers for cell in row if pd.notna(cell)):
                        header_row = i
                        break

                if header_row:
                    df = pd.read_excel(path_file, sheet_name=sheet, header=header_row)
                    df = df.fillna('')

                    for idx, row in df.iterrows():
                        try:
                            row_data = {}
                            for header in headers:
                                if header in df.columns:
                                    row_data[header] = row[header]
                                else:
                                    if header == 'Стоимость услуги (гр.46=гр. 34-гр.36+гр.41+гр.43-гр.44-гр.45), ₽':
                                        for column in df.columns:
                                            if 'Стоимость услуги (' in column:
                                                row_data[header] = row[column]

                            client_id = convert_id(row_data.get('ID бизнес-аккаунта', None))
                            posting_number = convert_id(row_data.get('Номер заказа', None))
                            application_number = convert_id(row_data.get('Номер заявки на утилизацию', None)) \
                                                 or convert_id(row_data.get('Номер заявки на Маркете', None)) \
                                                 or convert_id(row_data.get('Номер кампании', None)) \
                                                 or convert_id(row_data.get('Номер возврата', None))
                            accrual_date = row_data.get('Дата оказания услуги', None) or row_data.get(
                                'Дата и время оказания услуги', None)
                            cost = row_data.get('Стоимость услуги (гр.46=гр. 34-гр.36+гр.41+гр.43-гр.44-гр.45), ₽', None) \
                                   or row_data.get('Стоимость услуги, ₽', None) \
                                   or row_data.get('Стоимость услуги', None) \
                                   or row_data.get('Постоплата, ₽', None) \
                                   or row_data.get('Стоимость платного хранения, ₽', None)
                            name_service = 'Платное хранение' if 'Платное хранение' in sheet else sheet
                            service = row_data.get('Услуга', None) or name_service

                            if accrual_date is not None:
                                accrual_date = datetime.strptime(accrual_date, '%Y-%m-%d %H:%M:%S').date()
                            if cost is not None:
                                cost = round(float(cost), 2)

                            entry = DataYaReport(client_id=client_id,
                                                 campaign_id=campaign_id,
                                                 posting_number=posting_number,
                                                 application_number=application_number,
                                                 vendor_code=row_data.get('Ваш SKU', None),
                                                 service=service,
                                                 accrual_date=accrual_date,
                                                 cost=cost)
                            result_data.append(entry)
                        except Exception:
                            continue
            else:
                logger.error(f'Лист "{sheet}" не найден в файле.')
        return result_data
    except Exception as e:
        logger.error(f'Ошибка при чтении файла {path_file}: {e}')


async def main_yandex_report(retries: int = 6) -> None:
    """
        Основная функция для обновления записей в базе данных.

        Получает список клиентов из базы данных, затем для каждого клиента добавляет записи за вчерашний день в таблицу `ya_report`.
    """
    try:
        db_conn = YaDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace='Yandex')
        api_key_set = {client.api_key for client in clients}
        for api_key in api_key_set:
            list_campaigns = await get_campaign_ids(api_key=api_key)
            db_conn.add_ya_campaigns(list_campaigns=list_campaigns)
            from_date = datetime.now(tz=timezone(timedelta(hours=3))) - timedelta(days=1)
            for campaign in sorted(list_campaigns, key=lambda x: x.client_id):

                client = db_conn.get_client(client_id=campaign.client_id)
                logger.info(f"За дату {from_date.date().isoformat()}")
                logger.info(f"Добавление в базу данных компании '{client.name_company}' магазина '{campaign.name}'")
                path_file = await report_generate(client_id=client.client_id,
                                                  campaign_id=campaign.campaign_id,
                                                  api_key=client.api_key,
                                                  from_date=from_date.date().isoformat())
                if path_file is not None:
                    list_reports = await add_yandex_report_entry(path_file=path_file)
                    db_conn.add_ya_report(client_id=campaign.client_id, list_reports=list_reports)
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
