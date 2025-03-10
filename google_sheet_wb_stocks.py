import os
import time
import logging

import gspread

from decimal import Decimal

from gspread.utils import ValueInputOption
from gspread_formatting import *
from sqlalchemy.exc import OperationalError
from datetime import date, datetime
from oauth2client.service_account import ServiceAccountCredentials

from database import WBDbConnection

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
PATH_JSON = os.path.join(PROJECT_ROOT, 'templates', 'service-account-432709-1178152e9e49.json')
PROJECT = 'Коэффициенты остатков'

COLOR_HEADER = {"red": 0.7, "green": 0.7, "blue": 0.7}
COLOR_HEADER2 = {"red": 0.7, "green": 0.9, "blue": 1}

COLOR_BAD = {"red": 1.0, "green": 0.4, "blue": 0.4}
COLOR_NORMAL = {"red": 1.0, "green": 0.6, "blue": 0.6}
COLOR_GOOD = {"red": 0.6, "green": 1.0, "blue": 0.6}

COLOR_FORMAT = {"red": 0.9, "green": 0.9, "blue": 0.9}
COLOR_FORMAT2 = {"red": 1, "green": 1, "blue": 1}

BORDER_STYLE = {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}}
BORDER_STYLE2 = {"style": "SOLID", "width": 2, "color": {"red": 0, "green": 0, "blue": 0}}
BORDER_STYLE3 = {"style": "SOLID", "width": 3, "color": {"red": 0, "green": 0, "blue": 0}}


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


def format_sheet(worksheet: gspread.Worksheet, spreadsheet: gspread.Spreadsheet, data: list) -> None:
    all_requests = []

    all_requests.append({"updateDimensionProperties": {"range": {"sheetId": worksheet.id,
                                                                 "dimension": "COLUMNS",
                                                                 "startIndex": 0,
                                                                 "endIndex": 4},
                                                       "properties": {"pixelSize": 210},
                                                       "fields": "pixelSize"}})

    all_requests.append({"updateDimensionProperties": {"range": {"sheetId": worksheet.id,
                                                                 "dimension": "COLUMNS",
                                                                 "startIndex": 4,
                                                                 "endIndex": len(data[0])},
                                                       "properties": {"pixelSize": 75},
                                                       "fields": "pixelSize"}})

    for idx, val in enumerate(data[0]):
        if isinstance(val, int):
            all_requests.append({"mergeCells": {"range": {"sheetId": worksheet.id,
                                                          "startRowIndex": 0,
                                                          "endRowIndex": 1,
                                                          "startColumnIndex": idx,
                                                          "endColumnIndex": idx + 4},
                                                "mergeType": "MERGE_ALL"}})
            all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                          "startRowIndex": 0,
                                                          "endRowIndex": 1,
                                                          "startColumnIndex": idx,
                                                          "endColumnIndex": idx + 1},
                                                "cell": {"userEnteredFormat": {"numberFormat": {
                                                    "type": "DATE",
                                                    "pattern": "dd.mm.yyyy"}}
                                                },
                                                "fields": "userEnteredFormat.numberFormat"}})

    all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                  "startRowIndex": 0,
                                                  "endRowIndex": 2,
                                                  "startColumnIndex": 0,
                                                  "endColumnIndex": len(data[0])},
                                        "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER",
                                                                       "verticalAlignment": "MIDDLE",
                                                                       "wrapStrategy": "WRAP",
                                                                       "textFormat": {"bold": True},
                                                                       "backgroundColor": COLOR_HEADER}},
                                        "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,"
                                                  "wrapStrategy,textFormat,backgroundColor)"}})

    all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                  "startRowIndex": 2,
                                                  "endRowIndex": len(data),
                                                  "startColumnIndex": 4,
                                                  "endColumnIndex": len(data[0])},
                                        "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER",
                                                                       "verticalAlignment": "MIDDLE",
                                                                       "wrapStrategy": "WRAP"}},
                                        "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,"
                                                  "wrapStrategy)"}})

    for idx, val in enumerate(data[0]):
        if (val and idx) or idx in [0, 1, 2, 3, len(data[0]) - 1]:
            if not val:
                idx += 1
            all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                             "startRowIndex": 0,
                                                             "endRowIndex": len(data),
                                                             "startColumnIndex": idx,
                                                             "endColumnIndex": idx + 1},
                                                   "left": BORDER_STYLE3}})
        else:
            all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                             "startRowIndex": 0,
                                                             "endRowIndex": len(data),
                                                             "startColumnIndex": idx,
                                                             "endColumnIndex": idx + 1},
                                                   "left": BORDER_STYLE}})

    for idx, val in enumerate(data[1:], 1):
        try:
            if val[0] != data[idx + 1][0]:
                all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                                 "startRowIndex": idx if idx != 1 else 0,
                                                                 "endRowIndex": idx + 1,
                                                                 "startColumnIndex": 0,
                                                                 "endColumnIndex": len(data[0])},
                                                       "bottom": BORDER_STYLE3}})
            elif val[1] != data[idx + 1][1]:
                all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                                 "startRowIndex": idx,
                                                                 "endRowIndex": idx + 1,
                                                                 "startColumnIndex": 1,
                                                                 "endColumnIndex": len(data[0])},
                                                       "bottom": BORDER_STYLE2}})
            elif val[2] != data[idx + 1][2]:
                all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                                 "startRowIndex": idx,
                                                                 "endRowIndex": idx + 1,
                                                                 "startColumnIndex": 2,
                                                                 "endColumnIndex": len(data[0])},
                                                       "bottom": BORDER_STYLE}})
        except IndexError:
            all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                             "startRowIndex": idx,
                                                             "endRowIndex": idx + 1,
                                                             "startColumnIndex": 0,
                                                             "endColumnIndex": len(data[0])},
                                                   "bottom": BORDER_STYLE3}})

    all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                  "startRowIndex": 1,
                                                  "endRowIndex": 2,
                                                  "startColumnIndex": 4,
                                                  "endColumnIndex": len(data[1])},
                                        "cell": {"userEnteredFormat": {"backgroundColor": COLOR_HEADER2}},
                                        "fields": "userEnteredFormat(backgroundColor)"}})

    all_requests.append({"updateSheetProperties": {"properties": {"sheetId": worksheet.id,
                                                                  "gridProperties": {"frozenRowCount": 2,
                                                                                     "frozenColumnCount": 4}},
                                                   "fields": "gridProperties.frozenRowCount,"
                                                             "gridProperties.frozenColumnCount"}})

    all_requests.append({"addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                                           "startRowIndex": 2,
                                                                           "endRowIndex": len(data),
                                                                           "startColumnIndex": 0,
                                                                           "endColumnIndex": len(data[0])}],
                                                               "booleanRule": {"condition": {
                                                                   "type": "CUSTOM_FORMULA",
                                                                   "values": [
                                                                       {"userEnteredValue": "=ISEVEN(ROW())"}
                                                                   ]},
                                                                   "format": {"backgroundColor": COLOR_FORMAT}}}}})

    all_requests.append({"addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                                           "startRowIndex": 2,
                                                                           "endRowIndex": len(data),
                                                                           "startColumnIndex": 0,
                                                                           "endColumnIndex": len(data[0])}],
                                                               "booleanRule": {"condition": {
                                                                   "type": "CUSTOM_FORMULA",
                                                                   "values": [
                                                                       {"userEnteredValue": "=ISODD(ROW())"}
                                                                   ]},
                                                                   "format": {"backgroundColor": COLOR_FORMAT2}}}}})

    for idx, val in enumerate(data[1]):
        if val not in ['Коэф.', 'Запас\nдней']:
            continue
        all_requests.append({
            "addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                              "startRowIndex": 2,
                                                              "endRowIndex": len(data),
                                                              "startColumnIndex": idx,
                                                              "endColumnIndex": idx + 1}],
                                                  "booleanRule": {"condition": {
                                                      "type": "NUMBER_LESS",
                                                      "values": [{"userEnteredValue": "1,01" if val == 'Коэф.' else "30,01"}]},
                                                      "format": {"backgroundColor": COLOR_BAD}}}}})

        all_requests.append({"addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                                               "startRowIndex": 2,
                                                                               "endRowIndex": len(data),
                                                                               "startColumnIndex": idx,
                                                                               "endColumnIndex": idx + 1}],
                                                                   "booleanRule": {"condition": {
                                                                       "type": "NUMBER_BETWEEN",
                                                                       "values": [{"userEnteredValue": "1,01" if val == 'Коэф.' else "30,01"},
                                                                                  {"userEnteredValue": "1,51" if val == 'Коэф.' else "45,01"}]},
                                                                       "format": {"backgroundColor": COLOR_NORMAL}}}}})

        all_requests.append({"addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                                               "startRowIndex": 2,
                                                                               "endRowIndex": len(data),
                                                                               "startColumnIndex": idx,
                                                                               "endColumnIndex": idx + 1}],
                                                                   "booleanRule": {"condition": {
                                                                       "type": "NUMBER_GREATER",
                                                                       "values": [{"userEnteredValue": "1,51" if val == 'Коэф.' else "45,01"}]},
                                                                       "format": {"backgroundColor": COLOR_GOOD}}}}})

    all_requests.append({"setBasicFilter": {"filter": {"range": {"sheetId": worksheet.id,
                                                                 "startRowIndex": 1,
                                                                 "endRowIndex": len(data),
                                                                 "startColumnIndex": 0,
                                                                 "endColumnIndex": 4}}}})

    # Отправляем запрос на форматирование
    spreadsheet.batch_update({"requests": all_requests})


def wb_stocks_ratio(db_conn: WBDbConnection):
    entry = []
    data_map = {}
    data = []
    records = db_conn.get_wb_stocks_ratio()
    for record in records:
        if record[4].startswith('wb') or 'Виртуальный' == record[8] or (not int(record[6]) and not int(record[7])):
            continue
        entry.append([convert_date(value) if isinstance(value, date) else value for value in record])
    for row in entry:
        client = f'{row[1]} "{row[2]}"'
        vendor_code = f'{row[4]}'
        warehouse = f'{row[5]}'
        region = f'{row[8]}'
        count_orders = int(row[6])
        count_stocks = int(row[7])

        data_map.setdefault(client, {})
        data_map[client].setdefault(vendor_code, {})
        data_map[client][vendor_code].setdefault((region, warehouse), {})
        data_map[client][vendor_code][(region, warehouse)][row[0]] = (count_orders, count_stocks)

    data.append(['', '', '', ''])
    data.append(['ИП', 'Артикул', 'Регион', 'Склад'])

    for client, vendor_code_map in sorted(data_map.items()):
        for vendor_code, warehouse_map in sorted(vendor_code_map.items()):
            for (region, warehouse), date_map in sorted(warehouse_map.items()):
                data.append([client, vendor_code, region, warehouse])
                for date_ratio, (count_orders, count_stocks) in sorted(date_map.items(), reverse=True):
                    if len(data[0]) < 32:
                        data[0].extend([date_ratio, '', '', ''])
                        data[1].extend(['Заказы\n(30 дней)', 'Остаток\nна складе', 'Коэф.', 'Запас\nдней'])
                    col_count_orders = column_to_letter(len(data[-1]) + 1)
                    col_count_stocks = column_to_letter(len(data[-1]) + 2)
                    idx_row = len(data)

                    formula_ratio = f'=ЕСЛИ({col_count_stocks}{idx_row}=0; 0; ' \
                                    f'ОКРУГЛ({col_count_stocks}{idx_row}/МАКС({col_count_orders}{idx_row}; 5); 2))'
                    formula_reserve = f'=ЕСЛИ({col_count_stocks}{idx_row}=0; 0; ОКРУГЛ({col_count_stocks}{idx_row}/' \
                                      f'(МАКС({col_count_orders}{idx_row}; 5)/30); 2))'

                    data[-1].extend([count_orders, count_stocks, formula_ratio, formula_reserve])

    if entry:
        sheet_name = 'Коэффициенты WB'

        creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_JSON, SCOPE)
        client = gspread.authorize(creds)
        spreadsheet = client.open(PROJECT)

        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=5, cols=len(data[0]) + 5)

        total_rows = len(worksheet.get_all_values())
        if total_rows > 1:
            worksheet.delete_rows(2, total_rows)
        worksheet.clear()
        body = {"requests": [{"updateCells": {"range": {"sheetId": worksheet.id},
                                              "fields": "userEnteredFormat"}}]}
        worksheet.spreadsheet.batch_update(body)

        worksheet.insert_rows(data, 1, value_input_option=ValueInputOption.user_entered)
        try:
            worksheet.delete_rows(len(data) + 1)
        except Exception as e:
            print(e)

        format_sheet(spreadsheet=spreadsheet,
                     worksheet=worksheet,
                     data=data)


def main(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()
        db_conn.start_db()

        wb_stocks_ratio(db_conn=db_conn)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            time.sleep(10)
            main(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')


if __name__ == "__main__":
    main()
