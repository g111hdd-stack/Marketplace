import io
import csv
import uuid
import asyncio
import logging
import zipfile
import gspread
import nest_asyncio

from typing import Type
from gspread_formatting import *
from sqlalchemy.exc import OperationalError
from datetime import date, timedelta, datetime
from oauth2client.service_account import ServiceAccountCredentials

from wb_sdk.wb_api import WBApi
from database import WBDbConnection, Client

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
PATH_JSON = 'templates/service-account-432709-1178152e9e49.json'
PROJECT = 'Воронка'


def convert_date(x):
    if isinstance(x, str):
        x = datetime.strptime(x, '%Y-%m-%d').date()

    if isinstance(x, date):
        epoch = date(1899, 12, 30)
        delta = x - epoch
        return delta.days + (delta.seconds / 86400)

    return x


def column_to_letter(column: int):
    letters = []
    while column > 0:
        column, remainder = divmod(column - 1, 26)
        letters.append(chr(65 + remainder))
    return "".join(letters[::-1])


async def stat_card_update(db_conn: WBDbConnection, clients: list[Type[Client]]) -> None:
    entry = []

    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=31)

    for client in clients:
        new_uuid = str(uuid.uuid4())

        api_user = WBApi(api_key=client.api_key)

        answer_report = await api_user.get_mm_report_downloads(uuid=new_uuid,
                                                               start_date=start_date.isoformat(),
                                                               end_date=end_date.isoformat())
        if not answer_report.error:
            await asyncio.sleep(5)
            answer_download = await api_user.get_nm_report_downloads_file(uuid=new_uuid)
            zip_file = io.BytesIO(answer_download.file)
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                csv_filename = zip_ref.namelist()[0]
                with zip_ref.open(csv_filename) as csv_file:
                    csv_reader = csv.DictReader(io.TextIOWrapper(csv_file, encoding='utf-8'))
                    data = [row for row in csv_reader]
                    skus = db_conn.get_wb_sku_vendor_code(client_id=client.client_id)
                    for row in data:
                        sku = row.get('nmID', 0)
                        new = [
                            int(sku),
                            skus.get(sku, 'unknown'),
                            client.entrepreneur,
                            convert_date(row.get('dt')),
                            int(row.get('openCardCount', 0)),
                            int(row.get('addToCartCount', 0)),
                            int(row.get('ordersCount', 0)),
                            int(row.get('buyoutsCount', 0)),
                            int(row.get('cancelCount', 0)),
                            int(row.get('ordersSumRub', 0))
                        ]
                        entry.append(new)

    if entry:
        sheet_name = 'Статистика карточек WB'

        creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_JSON, SCOPE)
        client = gspread.authorize(creds)
        spreadsheet = client.open(PROJECT)

        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            headers = [
                'Артикул WB',
                'Артикул',
                'Магазин',
                'Дата',
                'Переходы в карточку',
                'Добавление в корзину',
                'Заказы',
                'Выкупы',
                'Отмены',
                'Сумма заказов'
            ]
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(headers) + 1)
            worksheet.insert_row(headers, 1)

        worksheet.delete_rows(2, len(worksheet.get_all_values()))

        worksheet.insert_rows(entry, 2)

        headers_sheet = worksheet.row_values(1)
        header_indices = {header: index for index, header in enumerate(headers_sheet, 1)}

        idx = header_indices['Дата']
        date_format = CellFormat(numberFormat=NumberFormat(type='DATE', pattern='yyyy-mm-dd'))
        cl = column_to_letter(idx)
        format_cell_range(worksheet, f'{cl}2:{cl}{len(entry) + 1}', date_format)


async def remains_update(clients: list[Type[Client]]):
    entry = []

    for client in clients:
        api_user = WBApi(api_key=client.api_key)

        answer_report = await api_user.get_warehouse_remains(group_by_nm=True)

        task_id = answer_report.data.taskId

        while True:
            await asyncio.sleep(10)
            answer_status_report = await api_user.get_warehouse_remains_tasks_status(task_id=task_id)

            status = answer_status_report.data.status
            if status == 'done':
                break
            elif status in ['canceled', 'purged']:
                logger.error(f"Ошибка отчёта по остаткам на складах {client.name_company}")
                break

        if status != 'done':
            continue

        answer_download_report = await api_user.get_warehouse_remains_tasks_download(task_id=task_id)

        for row in answer_download_report.result:
            new = [
                client.entrepreneur,
                row.nmId,
                row.quantityWarehousesFull,
                row.inWayToClient,
                row.inWayFromClient
            ]
            entry.append(new)

    if entry:
        sheet_name = 'Остатки на складах WB'

        creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_JSON, SCOPE)
        client = gspread.authorize(creds)
        spreadsheet = client.open(PROJECT)

        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            headers = [
                'Магазин',
                'Артикул WB',
                'Остаток',
                'В пути к клиенту',
                'В пути от клиента'
            ]
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(headers) + 1)
            worksheet.insert_row(headers, 1)

        worksheet.delete_rows(2, len(worksheet.get_all_values()))

        worksheet.insert_rows(entry, 2)


async def stat_advert_update(clients: list[Type[Client]]):
    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=31)
    sd = start_date

    entry = []
    date_list = []

    while sd <= end_date:
        date_list.append(sd.isoformat())
        sd += timedelta(days=1)

    for client in clients:
        adverts = {}

        status_dict = {
            7: 'Кампания завершена',
            9: 'Идут показы',
            11: 'Кампания на паузе'
        }

        type_dict = {
            8: 'Автоматическая кампания',
            9: 'Аукцион'
        }
        
        api_user = WBApi(api_key=client.api_key)

        for status in status_dict.keys():
            for type_field in type_dict.keys():
                answer_promotion = await api_user.get_promotion_adverts(status=status, type_field=type_field)
                if answer_promotion:
                    for advert in answer_promotion.result:
                        change_date = advert.changeTime.split('T')[0]
                        create_date = advert.createTime.split('T')[0]
                        ending_date = advert.endTime.split('T')[0]
                        if change_date >= start_date.isoformat() or status == 9:
                            id_advert = advert.advertId

                            adverts[id_advert] = [
                                client.entrepreneur,
                                id_advert,
                                advert.name or 'unknown',
                                type_dict.get(advert.type, 'unknown'),
                                create_date,
                                ending_date
                                ]
        if adverts:
            company_ids = list(adverts.keys())
            for dates in [date_list[i:i + 10] for i in range(0, len(date_list), 10)]:
                filter_company_ids = []
                for company_id in company_ids:
                    create = adverts.get(company_id)[-2]
                    end = adverts.get(company_id)[-1]
                    if not all(create > d for d in dates):
                        if not all(end < d for d in dates):
                            filter_company_ids.append(company_id)
                if not filter_company_ids:
                    continue
                for ids in [filter_company_ids[i:i + 100] for i in range(0, len(filter_company_ids), 100)]:
                    answer_stat = await api_user.get_fullstats(company_ids=ids, dates=dates)
                    if answer_stat:
                        for stat in answer_stat.result:
                            for day in stat.days:
                                data_sku = {}
                                if all([len(app.nm) == 1 for app in day.apps]) and len({app.nm[0].nmId for app in day.apps}) == 1:
                                    data_sku[day.apps[0].nm[0].nmId] = [day.views or 0, day.clicks or 0, day.sum or 0]
                                else:
                                    for app in day.apps:
                                        if len(app.nm) == 1:
                                            if data_sku.get(app.nm[0].nmId):
                                                data_sku[app.nm[0].nmId][0] += app.views or 0
                                                data_sku[app.nm[0].nmId][1] += app.clicks or 0
                                                data_sku[app.nm[0].nmId][2] += app.sum or 0
                                            else:
                                                data_sku[app.nm[0].nmId] = [app.views or 0, app.clicks or 0, app.sum or 0]
                                            continue
                                        for nm in app.nm:
                                            if data_sku.get(nm.nmId):
                                                data_sku[nm.nmId][0] += nm.views or 0
                                                data_sku[nm.nmId][1] += nm.clicks or 0
                                                data_sku[nm.nmId][2] += nm.sum or 0
                                            else:
                                                data_sku[nm.nmId] = [nm.views or 0, nm.clicks or 0, nm.sum or 0]

                                for sku, val in data_sku.items():
                                    new = [
                                        *adverts.get(stat.advertId)[:-2],
                                        sku,
                                        convert_date(day.date_field.date()),
                                        *val
                                    ]
                                    entry.append(new)

    if entry:
        sheet_name = 'Статистика РК WB'

        creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_JSON, SCOPE)
        client = gspread.authorize(creds)
        spreadsheet = client.open(PROJECT)

        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            headers = [
                'Магазин',
                'РК ID',
                'Наименование',
                'Тип',
                'Артикул WB',
                'Дата',
                'Просмотры',
                'Клики',
                'Расходы'
            ]
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(headers) + 1)
            worksheet.insert_row(headers, 1)

        worksheet.delete_rows(2, len(worksheet.get_all_values()))

        worksheet.insert_rows(entry, 2)

        headers_sheet = worksheet.row_values(1)
        header_indices = {header: index for index, header in enumerate(headers_sheet, 1)}

        idx = header_indices['Дата']
        date_format = CellFormat(numberFormat=NumberFormat(type='DATE', pattern='yyyy-mm-dd'))
        cl = column_to_letter(idx)
        format_cell_range(worksheet, f'{cl}2:{cl}{len(entry) + 1}', date_format)


async def main(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()
        db_conn.start_db()

        clients = db_conn.get_clients(marketplace="WB")
        db_conn.session.close()
        # await stat_card_update(db_conn=db_conn, clients=clients)
        await stat_advert_update(clients=clients)
        # await remains_update(clients=clients)

    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.stop()
