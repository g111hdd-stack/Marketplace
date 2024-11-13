import os
import time
import gspread
import logging

from contextlib import suppress
from datetime import date, timedelta
from gspread.utils import ValueInputOption
from sqlalchemy.exc import OperationalError
from oauth2client.service_account import ServiceAccountCredentials

from database import DbConnection

# Настройка
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

# Константы
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
PATH_JSON = os.path.join(PROJECT_ROOT, 'templates', 'service-account-432709-1178152e9e49.json')
PROJECT = 'Ежедневные заказы'

# Цветовые схемы
COLOR_HEADER = {"red": 0.75, "green": 0.85, "blue": 0.9}
COLOR_HEADER_MARKETS = {"Ozon": {"red": 0.7, "green": 0.8, "blue": 0.9},
                        "WB": {"red": 0.8, "green": 0.7, "blue": 0.9},
                        "Yandex": {"red": 0.9, "green": 0.8, "blue": 0.7}}
COLOR_HEADER_TOTAL = {"red": 0.65, "green": 0.75, "blue": 0.65}
COLOR_FIRST_COLUMN = {"red": 0.75, "green": 0.85, "blue": 0.9}
COLOR_MARKETS_DATA = {"Ozon": {"red": 0.91, "green": 0.96, "blue": 1.0},
                      "WB": {"red": 0.96, "green": 0.91, "blue": 1.0},
                      "Yandex": {"red": 1.0, "green": 0.96, "blue": 0.91}}
COLOR_MARKET_DATA = {"red": 0.91, "green": 0.96, "blue": 0.91}
COLOR_TOTAL_COLUMNS = {"red": 0.82, "green": 0.93, "blue": 0.82}
CATEGORY_ROW_COLOR = {"red": 0.88, "green": 0.88, "blue": 0.88}
TAB_COLOR_NEW_SHEET = {"red": 0, "green": 1, "blue": 0.33}
TAB_COLOR_COPY_SHEET = {"red": 1, "green": 1, "blue": 0}
TEXT_ROTATION_ANGLE = 40
HEADER_FONT_SIZE = 12
BORDER_STYLE = {"style": "SOLID", "width": 1, "color": {"red": 0, "green": 0, "blue": 0}}


def column_to_letter(column: int):
    letters = []
    while column > 0:
        column, remainder = divmod(column - 1, 26)
        letters.append(chr(65 + remainder))
    return "".join(letters[::-1])


def reorder_sheets(spreadsheet: gspread.Spreadsheet, pattern_name: str) -> None:
    """Реорганизация листов с сохранением шаблона в начале."""
    sheets = {sheet.title: sheet.id for sheet in spreadsheet.worksheets()}
    desired_order = list(sheets.keys())
    desired_order.remove(pattern_name)
    desired_order.sort(reverse=True, key=lambda x: (x.split(" копия")[0], "копия" not in x))
    desired_order = [pattern_name] + desired_order

    requests = []
    for index, sheet_name in enumerate(desired_order):
        sheet_id = sheets.get(sheet_name)
        if sheet_id is not None:
            requests.append({"updateSheetProperties": {"properties": {"sheetId": sheet_id, "index": index},
                                                       "fields": "index"}})
    if requests:
        spreadsheet.batch_update({"requests": requests})


def initialize_google_sheet() -> gspread.Spreadsheet:
    creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_JSON, SCOPE)
    client = gspread.authorize(creds)
    return client.open(PROJECT)


def hide_and_rename_existing_sheet(spreadsheet: gspread.Spreadsheet, worksheet_name: str) -> None:
    with suppress(gspread.exceptions.WorksheetNotFound):
        try:
            existing_sheet = spreadsheet.worksheet(worksheet_name)
            spreadsheet.batch_update(
                {"requests": [{"updateSheetProperties": {"properties": {"sheetId": existing_sheet.id,
                                                                        "hidden": True,
                                                                        "title": f"{worksheet_name} копия",
                                                                        "tabColor": TAB_COLOR_COPY_SHEET},
                                                         "fields": "title,hidden,tabColor"}}]})
        except gspread.exceptions.APIError as e:
            if 'Please enter another name' in e.response.text:
                spreadsheet.del_worksheet(existing_sheet)


def format_sheet(worksheet: gspread.Worksheet, spreadsheet: gspread.Spreadsheet, data: list, col_map: dict,
                 marketplaces: list) -> None:
    all_requests = []  # Список запросов на форматирование

    col_total_i = col_map["Итого"]["index"]
    col_total_stock_i = col_map["Итого остаток"]["index"]

    # Форматируем заголовки задаём шрифт, цвет и выравниваем по середине
    all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                  "startRowIndex": 0,
                                                  "endRowIndex": 1},
                                        "cell": {"userEnteredFormat": {"textFormat": {"fontSize": HEADER_FONT_SIZE,
                                                                                      "bold": True},
                                                                       "horizontalAlignment": "CENTER",
                                                                       "verticalAlignment": "MIDDLE",
                                                                       "wrapStrategy": "WRAP",
                                                                       "backgroundColor": COLOR_HEADER}},
                                        "fields": "userEnteredFormat(textFormat, horizontalAlignment, "
                                                  "verticalAlignment, wrapStrategy, backgroundColor)"}})

    # Для каждой обязательной колонки задаём ширину
    for enum, header in enumerate([data[0][0], *data[0][-3:]], 1):
        all_requests.append({
            "updateDimensionProperties": {"range": {"sheetId": worksheet.id,
                                                    "dimension": "COLUMNS",
                                                    "startIndex": col_map[header]['index'] - 1,
                                                    "endIndex": col_map[header]['index']},
                                          "properties": {"pixelSize": 125 if enum > 2 else 225},
                                          "fields": "pixelSize"}})

    # Для остальных колонок задаём ширину
    all_requests.append({"updateDimensionProperties": {"range": {"sheetId": worksheet.id,
                                                                 "dimension": "COLUMNS",
                                                                 "startIndex": 1,
                                                                 "endIndex": col_total_stock_i},
                                                       "properties": {"pixelSize": 110},
                                                       "fields": "pixelSize"}})

    # Задаём стиль границ для заголовков
    all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                     "startRowIndex": 0,
                                                     "endRowIndex": 1},
                                           "top": BORDER_STYLE,
                                           "bottom": BORDER_STYLE,
                                           "left": BORDER_STYLE,
                                           "right": BORDER_STYLE,
                                           "innerHorizontal": BORDER_STYLE,
                                           "innerVertical": BORDER_STYLE}})

    # Закрепляем заголовки и первый столбец
    all_requests.append({"updateSheetProperties": {"properties": {"sheetId": worksheet.id,
                                                                  "gridProperties": {"frozenRowCount": 1}},
                                                   "fields": "gridProperties.frozenRowCount"}})
    all_requests.append({"updateSheetProperties": {"properties": {"sheetId": worksheet.id,
                                                                  "gridProperties": {"frozenColumnCount": 1}},
                                                   "fields": "gridProperties.frozenColumnCount"}})

    # Задаём высоту первой строки
    all_requests.append({"updateDimensionProperties": {"range": {"sheetId": worksheet.id,
                                                                 "dimension": "ROWS",
                                                                 "startIndex": 0,
                                                                 "endIndex": 1},
                                                       "properties": {"pixelSize": 70},
                                                       "fields": "pixelSize"}})

    # Выравниваем по центру данные
    all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                  "startRowIndex": 1,
                                                  "endColumnIndex": col_total_stock_i},
                                        "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                                        "fields": "userEnteredFormat(horizontalAlignment)"}})

    # Задаём цвет для первой колонки
    all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                  "startRowIndex": 1,
                                                  "startColumnIndex": 0,
                                                  "endColumnIndex": 1},
                                        "cell": {"userEnteredFormat": {"backgroundColor": COLOR_FIRST_COLUMN}},
                                        "fields": "userEnteredFormat.backgroundColor"}})

    # Для каждого маркетплейса группируем магазины
    for marketplace in marketplaces:
        range_col = {"sheetId": worksheet.id,
                     "dimension": "COLUMNS",
                     "startIndex": col_map[marketplace]['index'],
                     "endIndex": max([val['index'] for name, val in col_map.items() if marketplace in name])}
        all_requests.append({"addDimensionGroup": {"range": range_col}})

        all_requests.append({"updateDimensionProperties": {"range": range_col,
                                                           "properties": {"hiddenByUser": True},
                                                           "fields": "hiddenByUser"}})

        indexes = [val['index'] for name, val in col_map.items() if marketplace in name]

        # Задаём цвет для колонок с данными по магазинам
        all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                      "startRowIndex": 1,
                                                      "startColumnIndex": min(indexes) - 1,
                                                      "endColumnIndex": max(indexes)},
                                            "cell": {"userEnteredFormat": {
                                                "backgroundColor": COLOR_MARKETS_DATA.get(marketplace,
                                                                                          COLOR_MARKET_DATA)}},
                                            "fields": "userEnteredFormat.backgroundColor"}})
        all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                      "startRowIndex": 0,
                                                      "endRowIndex": 1,
                                                      "startColumnIndex": min(indexes) - 1,
                                                      "endColumnIndex": max(indexes)},
                                            "cell": {"userEnteredFormat": {
                                                "backgroundColor": COLOR_HEADER_MARKETS.get(marketplace,
                                                                                            COLOR_HEADER)}},
                                            "fields": "userEnteredFormat.backgroundColor"}})

    # Задаём цвет для колонок с итоговыми данными
    all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                  "startRowIndex": 0,
                                                  "endRowIndex": 1,
                                                  "startColumnIndex": col_total_i - 1,
                                                  "endColumnIndex": col_total_stock_i},
                                        "cell": {"userEnteredFormat": {"backgroundColor": COLOR_HEADER_TOTAL}},
                                        "fields": "userEnteredFormat.backgroundColor"}})
    all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                  "startRowIndex": 1,
                                                  "startColumnIndex": col_total_i - 1,
                                                  "endColumnIndex": col_total_stock_i},
                                        "cell": {"userEnteredFormat": {"backgroundColor": COLOR_TOTAL_COLUMNS}},
                                        "fields": "userEnteredFormat.backgroundColor"}})

    # Задаём цвет и границы для строк с категориями
    for idx, value in enumerate(data, 1):
        if len(value) == 1:
            all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                          "startRowIndex": idx - 1,
                                                          "endRowIndex": idx},
                                                "cell": {
                                                    "userEnteredFormat": {"backgroundColor": CATEGORY_ROW_COLOR}},
                                                "fields": "userEnteredFormat.backgroundColor"}})
            all_requests.append({"updateBorders": {"range": {"sheetId": worksheet.id,
                                                             "startRowIndex": idx - 1,
                                                             "endRowIndex": idx},
                                                   "top": BORDER_STYLE,
                                                   "bottom": BORDER_STYLE}})

    # Маркируем новую страницу цветом
    all_requests.append({"updateSheetProperties": {"properties": {"sheetId": worksheet.id,
                                                                  "tabColor": TAB_COLOR_NEW_SHEET},
                                                   "fields": "tabColor"}})

    # Отправляем запрос на форматирование
    spreadsheet.batch_update({"requests": all_requests})


def stat_orders_update(db_conn: DbConnection, days: int = 1) -> None:
    # Дата за которую формируется лист
    from_date = date.today() - timedelta(days=days)

    # Получаем статиску по заказам
    orders = db_conn.get_orders(from_date=from_date)

    # Получаем артикулы из БД
    vendors_in_database = db_conn.get_vendors()

    # Задаем имена шаблонного листа и создаваемого
    sheet_name = 'Шаблон'
    worksheet_name = from_date.isoformat()

    # Подключение к гугл таблицам
    spreadsheet = initialize_google_sheet()

    # Список данных для таблицы
    data = []

    worksheet = spreadsheet.worksheet(sheet_name)

    # Проверяем наличие листа, если уже создан создаём заново, первоначальный лист становится копией
    hide_and_rename_existing_sheet(spreadsheet, worksheet_name)

    # Создаём новый лист
    new_worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=10, cols=10)

    # Сортируем листы для удобства
    reorder_sheets(spreadsheet=spreadsheet, pattern_name=sheet_name)

    # Собираем данные из шаблона
    vendors = worksheet.col_values(1) + ['Остальное']
    comments = worksheet.col_values(2)
    counts = worksheet.col_values(3)
    delivery_dates = worksheet.col_values(4)

    markets = []  # Список магазинов
    marketplaces = []  # Список маркетплейсов
    data_map = {}  # Словарь для данных
    col_map = {}  # Словарь колонок с индексами

    # Сортировка данных из БД
    for order in sorted(orders, key=lambda x: x.vendor_code):
        # Добавление артиклулов отсутствующих в шаблоне
        vendor = order.vendor_code.strip().lower()
        if vendor not in [v.strip().lower() for v in vendors]:
            vendors.append(vendor)

        # Формирование списка магазинов
        market = f"{order.client.name_company}\n{order.client.marketplace}"
        if market not in markets:
            markets.append(market)

        # Формирование словаря данных
        data_map.setdefault(vendor, {})
        data_map[vendor][market] = order.orders_count

    # Сортировка магазинов по маркетплейсу и названию
    markets.sort(key=lambda x: (x.split()[-1], x.split()[0]))

    # Формирование строк данных
    for i, vendor in enumerate(vendors, 1):
        row = [vendor]

        # Строка с заголовками
        if i == 1:
            for market in markets:
                # Формировние списков маркетплейсов
                marketplace = market.split()[-1]
                if marketplace not in row:
                    marketplaces.append(marketplace)
                    row.append(marketplace)

                row.append(market)

            # Добавляем обязательные заголовки
            row += ['Итого', 'Оборачиваемость', 'Итого остаток', 'Комментарий', 'Кол-во', 'Дата прихода']

            # Формируем словарь заголовков с цифровыми и буквенными индексами
            for j, val in enumerate(row, 1):
                col_map[val] = {'index': j, 'letter': column_to_letter(j)}

            data.append(row)
            continue

        # Строки с категориями
        if vendor.strip().lower() not in vendors_in_database:
            data.append(row)
            continue

        # Строки с данными
        for market in markets:
            marketplace = market.split()[-1]
            # Для каждого маркетплейса лобавляем формулу суммы данных по магазинам
            if len(row) + 1 == col_map.get(marketplace, {}).get('index', 0):
                # Получаем буквенные индексы первого и последнего магазина по маркетплейсу
                letters = [val['letter'] for name, val in sorted(col_map.items(), key=lambda x: x[1]['index']) if
                           marketplace in name]
                row.append(f'=СУММ({letters[1]}{i}:{letters[-1]}{i})')
            # Добавляем данные по магазинам
            row.append(data_map.get(vendor.strip().lower(), {}).get(market, 0))

        # Добавляем формулу итоговой суммы данных по всем маркетплейсам
        row.append(
            f'''=СУММ({"; ".join([f"{col_map[marketplace]['letter']}{i}" for marketplace in marketplaces])})''')

        col_total = col_map["Итого"]["letter"]
        col_total_stock_l = col_map["Итого остаток"]["letter"]

        # Добавляем формулу оборачиваемости
        row.append(f'=ЕСЛИ({col_total}{i}=0; 0; ОКРУГЛ({col_total_stock_l}{i}/{col_total}{i}; 0))')

        # Добавляем формулу итоговых остатков
        prev_sheet = (from_date - timedelta(days=1)).isoformat()
        row.append(
            f"""=ЕСЛИОШИБКА(ВПР(A{i};ДВССЫЛ("'{prev_sheet}'!$A$1:$WW$1000");"""
            f"""ПОИСКПОЗ({col_total_stock_l}1;ДВССЫЛ("'{prev_sheet}'!$A$1:$WW$1");0);ЛОЖЬ);0)-{col_total}{i}""")

        # Добавляем данные из шаблона из столбцов Комментарий, Кол-во, Дата прихода
        row.append(next(iter(comments[i - 1:i]), ''))
        row.append(next(iter(counts[i - 1:i]), ''))
        row.append(next(iter(delivery_dates[i - 1:i]), ''))

        data.append(row)

    # Записываем данные в гугл таблицу
    new_worksheet.update(range_name='A1', values=data, value_input_option=ValueInputOption("USER_ENTERED"))

    # Форматируем лист
    format_sheet(spreadsheet=spreadsheet,
                 worksheet=new_worksheet,
                 data=data,
                 col_map=col_map,
                 marketplaces=marketplaces)


def main(retries: int = 6) -> None:
    try:
        db_conn = DbConnection()
        db_conn.start_db()

        stat_orders_update(db_conn=db_conn, days=1)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            time.sleep(10)
            main(retries=retries - 1)
    except gspread.exceptions.APIError as e:
        logger.error(f'Ошибка работы с GoogleSheet: {e}. Осталось попыток: {retries - 1}')
        if retries > 0:
            time.sleep(60)
            main(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')


if __name__ == "__main__":
    main()
