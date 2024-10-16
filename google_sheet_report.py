import asyncio
import logging
import gspread
import nest_asyncio

from typing import Type
from decimal import Decimal
from gspread_formatting import *
from sqlalchemy.exc import OperationalError
from datetime import date, datetime
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
        return int(delta.days + (delta.seconds / 86400))

    return x


def column_to_letter(column: int):
    letters = []
    while column > 0:
        column, remainder = divmod(column - 1, 26)
        letters.append(chr(65 + remainder))
    return "".join(letters[::-1])


async def stat_card_update(db_conn: WBDbConnection) -> None:
    entry = []
    records = db_conn.get_wb_stat_card_google()
    for record in records:
        entry.append(
            [convert_date(value) if isinstance(value, date) else int(value) if isinstance(value, Decimal) else value
             for value in record])

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


async def stat_advert_update(db_conn: WBDbConnection):
    entry = []
    records = db_conn.get_wb_stat_advert_google()
    for record in records:
        entry.append(
            [convert_date(value) if isinstance(value, date) else float(value) if isinstance(value, Decimal) else value
             for value in record])

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
        await stat_card_update(db_conn=db_conn)
        await stat_advert_update(db_conn=db_conn)
        await remains_update(clients=clients)

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
