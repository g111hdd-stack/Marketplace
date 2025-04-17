import os
import time
import gspread
import logging
import requests
import pandas as pd

from datetime import date, datetime
from gspread.utils import ValueInputOption
from sqlalchemy.exc import OperationalError
from oauth2client.service_account import ServiceAccountCredentials

from database import WBDbConnection
from config import TOKEN, CHAT_ID, LINK

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
PATH_JSON = os.path.join(PROJECT_ROOT, 'templates', 'service-account-432709-1178152e9e49.json')
PROJECT = 'Коэффициенты остатков'

COLOR_HEADER = {"red": 0.7, "green": 0.7, "blue": 0.7}
COLOR_HEADER2 = {"red": 0.7, "green": 0.9, "blue": 1}

COLOR_GOOD = {"red": 0.376, "green": 0.827, "blue": 0.580}  # #60D394 (Зеленый)
COLOR_NORMAL = {"red": 1.0, "green": 0.850, "blue": 0.490}  # #FFD97D (Желтый)
COLOR_BAD = {"red": 1.0, "green": 0.608, "blue": 0.521}  # #FF9B85 (Красный)

COLOR_FORMAT = {"red": 0.9, "green": 0.9, "blue": 0.9}
COLOR_FORMAT2 = {"red": 1, "green": 1, "blue": 1}

BORDER_STYLE = {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}}
BORDER_STYLE2 = {"style": "SOLID", "width": 2, "color": {"red": 0, "green": 0, "blue": 0}}
BORDER_STYLE3 = {"style": "SOLID", "width": 3, "color": {"red": 0, "green": 0, "blue": 0}}

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def check(ratio: float = None, local: float = None):
    if ratio is not None:
        val = ratio
        bad = 1.01
        good = 1.51
    elif local is not None:
        val = local
        bad = 50.01
        good = 70.01
    else:
        return ""

    if val < bad:
        return "🔴"
    if bad <= val < good:
        return "🟠"
    if val >= good:
        return "🟢"


def request_telegram(mes: str):
    response = requests.post(URL, data={"chat_id": CHAT_ID, "text": mes, "parse_mode": "Markdown"})
    for _ in range(3):
        if response.status_code == 200:
            break
        else:
            time.sleep(1)
    else:
        print(f"Неудалось отправить сообщение: {mes}")
        print(f"Ошибка {response.status_code}")


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
                                                  "startRowIndex": 2,
                                                  "endRowIndex": len(data),
                                                  "startColumnIndex": 0,
                                                  "endColumnIndex": 4},
                                        "cell": {"userEnteredFormat": {"numberFormat": {"type": "TEXT"}}},
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
                                                      "values": [
                                                          {"userEnteredValue": "1,01" if val == 'Коэф.' else "30,01"}]},
                                                      "format": {"backgroundColor": COLOR_BAD}}}}})

        all_requests.append({"addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                                               "startRowIndex": 2,
                                                                               "endRowIndex": len(data),
                                                                               "startColumnIndex": idx,
                                                                               "endColumnIndex": idx + 1}],
                                                                   "booleanRule": {"condition": {
                                                                       "type": "NUMBER_BETWEEN",
                                                                       "values": [
                                                                           {"userEnteredValue": "1,01" if val == 'Коэф.' else "30,01"},
                                                                           {"userEnteredValue": "1,51" if val == 'Коэф.' else "45,01"}]},
                                                                       "format": {"backgroundColor": COLOR_NORMAL}}}}})

        all_requests.append({"addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                                               "startRowIndex": 2,
                                                                               "endRowIndex": len(data),
                                                                               "startColumnIndex": idx,
                                                                               "endColumnIndex": idx + 1}],
                                                                   "booleanRule": {"condition": {
                                                                       "type": "NUMBER_GREATER",
                                                                       "values": [{
                                                                           "userEnteredValue": "1,51" if val == 'Коэф.' else "45,01"}]},
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
        entry.append([convert_date(value) if isinstance(value, date) else value for value in record])
    for row in entry:
        client = f'{row[1]} "{row[2]}"'
        vendor_code = f'{row[3]}'
        warehouse = f'{row[4]}'
        region = f'{row[7]}'
        count_orders = int(row[5])
        count_stocks = int(row[6])

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
                    if not count_orders and not count_stocks:
                        data.pop()
                        break

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
        spreadsheet.batch_update(body)

        worksheet.insert_rows(data, 1, value_input_option=ValueInputOption.user_entered)
        try:
            worksheet.delete_rows(len(data) + 1)
        except Exception as e:
            print(e)

        format_sheet(spreadsheet=spreadsheet,
                     worksheet=worksheet,
                     data=data)


def format_sheet2(worksheet: gspread.Worksheet, spreadsheet: gspread.Spreadsheet, data: list, new: bool) -> None:
    all_requests = []

    all_requests.append({"updateDimensionProperties": {"range": {"sheetId": worksheet.id,
                                                                 "dimension": "COLUMNS",
                                                                 "startIndex": 0,
                                                                 "endIndex": 3},
                                                       "properties": {"pixelSize": 210},
                                                       "fields": "pixelSize"}})

    all_requests.append({"updateDimensionProperties": {"range": {"sheetId": worksheet.id,
                                                                 "dimension": "COLUMNS",
                                                                 "startIndex": 3,
                                                                 "endIndex": len(data[0])},
                                                       "properties": {"pixelSize": 90},
                                                       "fields": "pixelSize"}})

    all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                  "startRowIndex": 0,
                                                  "endRowIndex": 1,
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
                                                  "startRowIndex": 1,
                                                  "endRowIndex": len(data),
                                                  "startColumnIndex": 3,
                                                  "endColumnIndex": len(data[0])},
                                        "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER",
                                                                       "verticalAlignment": "MIDDLE",
                                                                       "wrapStrategy": "WRAP"}},
                                        "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment,"
                                                  "wrapStrategy)"}})

    all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                  "startRowIndex": 1,
                                                  "endRowIndex": len(data),
                                                  "startColumnIndex": 19,
                                                  "endColumnIndex": 20},
                                        "cell": {"userEnteredFormat": {"numberFormat": {"type": "PERCENT",
                                                                                        "pattern": "0.00%"}}},
                                        "fields": "userEnteredFormat.numberFormat"}})

    all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                  "startRowIndex": 1,
                                                  "endRowIndex": len(data),
                                                  "startColumnIndex": 0,
                                                  "endColumnIndex": 3},
                                        "cell": {"userEnteredFormat": {"numberFormat": {"type": "TEXT"}}},
                                        "fields": "userEnteredFormat.numberFormat"}})

    all_requests.append({"setDataValidation": {"range": {"sheetId": worksheet.id,
                                                         "startRowIndex": 1,
                                                         "endRowIndex": len(data),
                                                         "startColumnIndex": len(data[0]) - 1,
                                                         "endColumnIndex": len(data[0])},
                                               "rule": {"condition": {
                                                       "type": "BOOLEAN"},
                                                   "inputMessage": "Выберите значение",
                                                   "strict": True,
                                                   "showCustomUi": True}}})

    for idx, val in enumerate(data[0]):
        if idx < 5 or idx == 15:
            all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                             "startRowIndex": 0,
                                                             "endRowIndex": len(data),
                                                             "startColumnIndex": idx,
                                                             "endColumnIndex": idx + 1},
                                                   "left": BORDER_STYLE2}})
        else:
            all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                             "startRowIndex": 0,
                                                             "endRowIndex": len(data),
                                                             "startColumnIndex": idx,
                                                             "endColumnIndex": idx + 1},
                                                   "left": BORDER_STYLE}})
    else:
        all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                         "startRowIndex": 0,
                                                         "endRowIndex": len(data),
                                                         "startColumnIndex": len(data[0]),
                                                         "endColumnIndex": len(data[0]) + 1},
                                               "left": BORDER_STYLE2}})

    for idx, val in enumerate(data):
        try:
            if val[0] != data[idx + 1][0]:
                all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                                 "startRowIndex": idx,
                                                                 "endRowIndex": idx + 1,
                                                                 "startColumnIndex": 0,
                                                                 "endColumnIndex": len(data[0])},
                                                       "bottom": BORDER_STYLE2}})
            elif val[1] != data[idx + 1][1]:
                all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                                 "startRowIndex": idx,
                                                                 "endRowIndex": idx + 1,
                                                                 "startColumnIndex": 1,
                                                                 "endColumnIndex": len(data[0])},
                                                       "bottom": BORDER_STYLE}})
        except IndexError:
            pass

    all_requests.append({"updateSheetProperties": {"properties": {"sheetId": worksheet.id,
                                                                  "gridProperties": {"frozenRowCount": 1,
                                                                                     "frozenColumnCount": 3}},
                                                   "fields": "gridProperties.frozenRowCount,"
                                                             "gridProperties.frozenColumnCount"}})

    all_requests.append({"addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                                           "startRowIndex": 1,
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
                                                                           "startRowIndex": 1,
                                                                           "endRowIndex": len(data),
                                                                           "startColumnIndex": 0,
                                                                           "endColumnIndex": len(data[0])}],
                                                               "booleanRule": {"condition": {
                                                                   "type": "CUSTOM_FORMULA",
                                                                   "values": [
                                                                       {"userEnteredValue": "=ISODD(ROW())"}
                                                                   ]},
                                                                   "format": {"backgroundColor": COLOR_FORMAT2}}}}})

    all_requests.append({"addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                                           "startRowIndex": 1,
                                                                           "endRowIndex": len(data),
                                                                           "startColumnIndex": 4,
                                                                           "endColumnIndex": 15}],
                                                               "booleanRule": {"condition": {
                                                                   "type": "CUSTOM_FORMULA",
                                                                   "values": [
                                                                       {"userEnteredValue": "=$C2=E$1"}
                                                                   ]},
                                                                   "format": {"backgroundColor": COLOR_GOOD}}}}})

    for idx, val in enumerate(data[0]):
        if val not in ['Коэф.', 'Локальных заказов', 'Запас\nдней']:
            continue

        values = {'bad': {'Коэф.': "1,01",
                          'Запас\nдней': "30,01",
                          'Локальных заказов': "0,501"},
                  'good': {'Коэф.': "1,51",
                           'Запас\nдней': "45,01",
                           'Локальных заказов': "0,701"}}

        all_requests.append({
            "addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                              "startRowIndex": 1,
                                                              "endRowIndex": len(data),
                                                              "startColumnIndex": idx,
                                                              "endColumnIndex": idx + 1}],
                                                  "booleanRule": {"condition": {
                                                      "type": "NUMBER_LESS",
                                                      "values": [
                                                          {"userEnteredValue": values['bad'][val]}]},
                                                      "format": {"backgroundColor": COLOR_BAD}}}}})

        all_requests.append({"addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                                               "startRowIndex": 1,
                                                                               "endRowIndex": len(data),
                                                                               "startColumnIndex": idx,
                                                                               "endColumnIndex": idx + 1}],
                                                                   "booleanRule": {"condition": {
                                                                       "type": "NUMBER_BETWEEN",
                                                                       "values": [{
                                                                           "userEnteredValue": values['bad'][val]},
                                                                           {
                                                                               "userEnteredValue": values['good'][
                                                                                   val]}]},
                                                                       "format": {"backgroundColor": COLOR_NORMAL}}}}})

        all_requests.append({"addConditionalFormatRule": {"rule": {"ranges": [{"sheetId": worksheet.id,
                                                                               "startRowIndex": 1,
                                                                               "endRowIndex": len(data),
                                                                               "startColumnIndex": idx,
                                                                               "endColumnIndex": idx + 1}],
                                                                   "booleanRule": {"condition": {
                                                                       "type": "NUMBER_GREATER",
                                                                       "values": [{
                                                                           "userEnteredValue": values['good'][val]}]},
                                                                       "format": {"backgroundColor": COLOR_GOOD}}}}})

    all_requests.append({"setBasicFilter": {"filter": {"range": {"sheetId": worksheet.id,
                                                                 "startRowIndex": 0,
                                                                 "endRowIndex": len(data),
                                                                 "startColumnIndex": 0,
                                                                 "endColumnIndex": 3}}}})

    range_col = {"sheetId": worksheet.id,
                 "dimension": "COLUMNS",
                 "startIndex": 4,
                 "endIndex": 15}
    if new:
        all_requests.append({"addDimensionGroup": {"range": range_col}})

    all_requests.append({"updateDimensionProperties": {"range": range_col,
                                                       "properties": {"hiddenByUser": True},
                                                       "fields": "hiddenByUser"}})

    # Отправляем запрос на форматирование
    spreadsheet.batch_update({"requests": all_requests})


def wb_stocks_ratio_buyer(db_conn):
    conn = db_conn.engine.raw_connection()
    query = """SELECT * FROM wb_stocks_ratio_buyer"""

    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()

    df = df.astype(str)

    sheet_name = 'Коэффициенты WB по складу покупателя'
    sheet_name_temp = 'Alert'

    creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_JSON, SCOPE)
    client = gspread.authorize(creds)
    spreadsheet = client.open(PROJECT)

    headers = [val.replace('\\n', '\n') for val in df.columns] + ['Коэф.', 'Локальных заказов', 'Запас\nдней', 'Alert']

    try:
        worksheet_temp = spreadsheet.worksheet(sheet_name_temp)
    except gspread.exceptions.WorksheetNotFound:
        worksheet_temp = spreadsheet.add_worksheet(title=sheet_name_temp, rows=100, cols=5)

    alerts_temp = list({tuple(val[:3]) for val in worksheet_temp.get_all_values() if all(val[:3])})

    try:
        new = False
        worksheet = spreadsheet.worksheet(sheet_name)
        alerts = {tuple(val[:3]): False if val[-1] == 'FALSE' else True
                  for val in worksheet.get_all_values() if val[-1] in ['FALSE', 'TRUE']}

    except gspread.exceptions.WorksheetNotFound:
        new = True
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=5, cols=len(headers) + 5)
        alerts = {}

    for k, v in alerts.items():
        if v and k not in alerts_temp:
            alerts_temp.append(k)
        elif not v and k in alerts_temp:
            alerts_temp.remove(k)

    alerts_temp = [list(val) for val in alerts_temp]
    worksheet_temp.clear()
    worksheet_temp.update(alerts_temp)

    values = [val.tolist() +
              [f'=ЕСЛИ(R{idx}=0; 0; ОКРУГЛ(R{idx}/МАКС(D{idx}; 5); 2))',
               f'=ЕСЛИ(P{idx}=0; 0; ОКРУГЛ(P{idx}/D{idx}; 4))',
               f'=ЕСЛИ(R{idx}=0; 0; ОКРУГЛ(R{idx}/(МАКС(D{idx}; 5)/30); 2))',
               True if val.tolist()[:3] in alerts_temp else False] for idx, val in enumerate(df.values, 2)]

    data = [headers] + values

    sorted_indices = sorted(range(4, 15), key=lambda x: data[0][x])

    for i in range(len(data)):
        data[i][4:15] = [data[i][j] for j in sorted_indices]

    total_rows = len(worksheet.get_all_values())
    if total_rows > 1:
        worksheet.insert_row([''], index=total_rows)
        worksheet.delete_rows(2, total_rows)
    worksheet.clear()
    body = {"requests": [{"updateCells": {"range": {"sheetId": worksheet.id},
                                          "fields": "userEnteredFormat"}}]}
    spreadsheet.batch_update(body)

    worksheet.insert_rows(data, 1, value_input_option=ValueInputOption.user_entered)

    format_sheet2(spreadsheet=spreadsheet,
                  worksheet=worksheet,
                  data=data,
                  new=new)

    try:
        worksheet.delete_rows(len(data) + 1, worksheet.row_count)
    except Exception as e:
        print(e)

    len_alerts_temp = len(alerts_temp)
    count_good = 0
    count_normal = 0
    count_bad = 0

    request_telegram(f"*Отчёт за {date.today().strftime('%d.%m.%Y')}*")

    for d in data:
        key = d[:3]

        if key in alerts_temp:
            alerts_temp.remove(key)

            try:
                ratio = round(int(d[17]) / max([int(d[3]), 5]), 2)
                stock = round(int(d[17]) / (max([int(d[3]), 5]) / 30), 2)
                local = round((int(d[15]) / max([int(d[3]), 1])) * 100, 2)
            except:
                continue

            color_1 = check(ratio=ratio)
            color_2 = check(local=local)
            if color_1 == "🟢" and color_2 == "🟢":
                count_good += 1
                continue
            elif color_1 == "🔴" or color_2 == "🔴":
                count_bad += 1
            else:
                count_normal += 1

            message = f"*ИП:* `{key[0]}`\n" \
                      f"*Артикул:* `{key[1]}`\n" \
                      f"*Регион:* `{key[2]}`\n" \
                      f"\n" \
                      f"*Заказы(30дней):* {d[3]}\n" \
                      f"*Остаток на складах:* {d[17]}\n" \
                      f"*Локально\\Не локально:* {d[15]}\\{d[16]}\n" \
                      f"\n" \
                      f"{color_1} *Коэфициент:* {ratio}\n" \
                      f"{color_1} *Запас в днях:* {stock}\n" \
                      f"{color_2} *Доля локальных:* {local}%\n"

            request_telegram(message)
    else:
        sub_text = ""
        if alerts_temp:
            sub_text = "\nУшли из отчёта:\n"
            for a in alerts_temp:
                sub_text += f"{a}\n"

        text = f"*Отслеживается:* {len_alerts_temp}" \
               f"\n" \
               f"*Из них:*\n" \
               f"🟢 {count_good}\n" \
               f"🟠 {count_normal}\n" \
               f"🔴 {count_bad}\n" \
               f"{sub_text}" \
               f"\n" \
               f"*Подробнее в* [Google Таблице]({LINK})"
        request_telegram(text)


def main(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()
        db_conn.start_db()

        wb_stocks_ratio_buyer(db_conn=db_conn)
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
