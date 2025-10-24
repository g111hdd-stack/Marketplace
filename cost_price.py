import os
import gspread
import logging
import datetime
import warnings
import pandas as pd

from sqlalchemy import create_engine, text
from oauth2client.service_account import ServiceAccountCredentials

from config import DB_URL

warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
PATH_JSON = os.path.join(PROJECT_ROOT, 'templates', 'service-account-432709-1178152e9e49.json')

HEADER_COLOR = {"red": 0.2, "green": 0.4, "blue": 0.6}
FIRST_BAND_COLOR = {"red": 0.9, "green": 0.95, "blue": 0.95}
SECOND_BAND_COLOR = {"red": 0.98, "green": 0.98, "blue": 1.0}

month = {
    1: 'январь',
    2: 'февраль',
    3: 'март',
    4: 'апрель',
    5: 'май',
    6: 'июнь',
    7: 'июль',
    8: 'август',
    9: 'сентябрь',
    10: 'октябрь',
    11: 'ноябрь',
    12: 'декабрь'
}

cloth = [
    "90001/зипкатемнсер",
    "90001/зипкасер",
    "90002/зипкачернбел",
    "90002/зипкасерчерн",
    "90000/комбелкрас",
    "90008/джинблеск",
    "90009/зипкакрем",
    "90010/комчер",
    "90011/комсер",
    "90013/костюмроз",
    "90014/блузкабант",
    "90015/боди",
    "90016/джинсрван",
    "90017/топодплечо",
    "90018/багги",
    "90019/джинсер",
    "90019/джинфил",
    "90020/тройкабел",
    "90020/тройкагол",
    "90021/шортыджинбел",
    "90021/шортыджинчер",
    "90022/двойкабел",
    "90000/комкорчер",
    "90003/комсерыйскап",
    "90004/комюбка",
    "90005/комдомроз",
    "90005/комдомгол",
    "90006/топсет",
    "90007/топшнур"
]

column = ['month_date', 'year_date', 'vendor_code', 'cost']


def get_values(to_date: datetime.date) -> list:
    creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_JSON, SCOPE)
    client = gspread.authorize(creds)
    spreadsheet = client.open('Расчет себестоимости')

    worksheets = spreadsheet.worksheets()

    to_year = to_date.year
    to_month = to_date.month

    sheet_name = next((worksheet.title for worksheet in worksheets if
                       str(to_year) in worksheet.title and month.get(
                           to_month) in worksheet.title.lower()), None)

    if sheet_name is None:
        logger.warning(f'Страница за {month.get(to_month).capitalize()} {to_year} не найдена')
        if to_month == 1:
            to_month = 12
            to_year -= 1
        else:
            to_month -= 1
        sheet_name = next((worksheet.title for worksheet in worksheets if
                           str(to_year) in worksheet.title and month.get(
                               to_month) in worksheet.title.lower()), None)

    if sheet_name is None:
        logger.error(f'Страница себестоимости не найдена')
        return []

    worksheet = spreadsheet.worksheet(sheet_name)

    data = worksheet.get_all_values()

    entry = []

    month_date = to_date.month
    year_date = to_date.year

    for row in data[1:]:
        try:
            vendor_code = row[0].lower().strip()
            if vendor_code not in cloth:
                cost = round(float(row[14].replace(',', '.') or row[1].replace(',', '.')), 2)
            else:
                cost = 0
            entry.append([month_date, year_date, vendor_code, cost])
        except Exception as e:
            logger.error(f'Ошибка получения данных строки {row}: {str(e)}')

    return [dict(zip(column, row)) for row in entry]


def cost_price():
    to_date = datetime.date.today()

    values = get_values(to_date=to_date)

    if not values:
        logger.error('Данные по себестоимости отсутствуют')
        return

    engine = create_engine(DB_URL)

    if to_date.day == 1:
        sql_pre_month = text("""
            INSERT INTO public.cost_price
                (month_date, year_date, vendor_code, cost)
            SELECT
                :month_date, :year_date, vendor_code, cost
            FROM public.cost_price
            WHERE month_date = :pre_month_date AND year_date = :pre_year_date
            ON CONFLICT (month_date, year_date, vendor_code) DO NOTHING
            RETURNING vendor_code
        """)

        with engine.begin() as conn:
            logger.info('Создаю новый месяц')
            result = conn.execute(sql_pre_month,
                                  {'month_date': to_date.month,
                                   'year_date': to_date.year,
                                   'pre_month_date': to_date.month - 1 or 12,
                                   'pre_year_date': to_date.year if to_date.month != 1 else to_date.year - 1})
            logger.info(f'Запись {len(result.fetchall())} строк успешно завершена')

    sql = text("""
        INSERT INTO public.cost_price
            (month_date, year_date, vendor_code, cost)
        VALUES
            (:month_date, :year_date, :vendor_code, :cost)
        ON CONFLICT (month_date, year_date, vendor_code) DO UPDATE
        SET cost = EXCLUDED.cost
    """)

    with engine.begin() as conn:
        logger.info('Вставляю новые записи в cost_price')
        conn.execute(sql, values)
        logger.info('Запись успешно завершена')

    sql_new_vendor_code = text("""
        INSERT INTO public.ip_vendor_code
            (vendor_code, "group")
        SELECT
            lower(vc.vendor_code), 'new'
        FROM vendor_code vc
        WHERE vc.vendor_code NOT LIKE '%---%'
        ON CONFLICT (vendor_code) DO NOTHING
        RETURNING vendor_code
    """)

    with engine.begin() as conn:
        logger.info('Вставляю новые артикулы в ip_vendor_code')
        result = conn.execute(sql_new_vendor_code)
        logger.info(f'Запись {len(result.fetchall())} строк успешно завершена')

    sql_update_cost_price = text("""
        INSERT INTO public.cost_price 
            (month_date, year_date, vendor_code, "cost")
        SELECT 
            :month_date AS month_date,
            :year_date AS year_date,
            ivc.vendor_code,
            cp.cost
        FROM public.ip_vendor_code ivc
        LEFT JOIN public.cost_price cp
            ON lower(cp.vendor_code) = lower(ivc.main_vendor_code) 
            AND cp.month_date = :month_date
            AND cp.year_date = :year_date
        WHERE (ivc."group" IS NULL OR ivc."group" <> 'other_trash')
            AND cp.cost IS NOT NULL 
            AND ivc.type_of_vendor_code = 'maindouble'
        ON CONFLICT (month_date, year_date, vendor_code) DO UPDATE
        SET cost = EXCLUDED.cost
    """)

    with engine.begin() as conn:
        logger.info('Обновляю записи по дублям')
        conn.execute(sql_update_cost_price, {'month_date': to_date.month, 'year_date': to_date.year})
        logger.info('Запись успешно завершена')


def write_google_accounting_cost():
    sheet_name = 'Косты'
    engine = create_engine(DB_URL)

    query = "SELECT month, year, vendor_code, cost FROM accounting_cost ORDER BY year desc, month desc, vendor_code"

    try:
        all_requests = []
        headers = [
            'Месяц',
            'Год',
            'Артикул',
            'Кост'
        ]

        logger.info("Считываю данные с БД.")
        df = pd.read_sql(query, engine)
        data_to_insert = df.values.tolist()

        logger.info("Подключаюсь к Google Таблице.")
        creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_JSON, SCOPE)
        client = gspread.authorize(creds)
        spreadsheet = client.open('Косты')

        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            logger.info(f"Создаю лист {sheet_name}.")
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=len(headers) + 1)

        logger.info("Очищаю от старых данных.")
        worksheet.delete_rows(1, len(worksheet.get_all_values()))
        logger.info("Начинаю запись.")
        worksheet.insert_row(headers, 1)
        worksheet.insert_rows(data_to_insert, 2)
        logger.info("Применяю стили.")
        all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                      "startRowIndex": 0,
                                                      "endRowIndex": 1,
                                                      "endColumnIndex": len(data_to_insert[1])},
                                            "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER",
                                                                           "verticalAlignment": "MIDDLE",
                                                                           "wrapStrategy": "WRAP"}},
                                            "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment, "
                                                      "wrapStrategy)"}})

        all_requests.append({"addBanding": {"bandedRange": {"range": {"sheetId": worksheet.id,
                                                                      "startRowIndex": 0,
                                                                      "endRowIndex": len(data_to_insert) + 1,
                                                                      "startColumnIndex": 0,
                                                                      "endColumnIndex": len(data_to_insert[0])},
                                                            "rowProperties": {"headerColor": HEADER_COLOR,
                                                                              "firstBandColor": FIRST_BAND_COLOR,
                                                                              "secondBandColor": SECOND_BAND_COLOR}}}})

        all_requests.append({"updateDimensionProperties": {"range": {"sheetId": worksheet.id,
                                                                     "dimension": "COLUMNS",
                                                                     "startIndex": 2,
                                                                     "endIndex": 3},
                                                           "properties": {"pixelSize": 300},
                                                           "fields": "pixelSize"}})

        all_requests.append({"setBasicFilter": {"filter": {"range": {"sheetId": worksheet.id,
                                                                     "startRowIndex": 0,
                                                                     "endRowIndex": len(data_to_insert) + 1,
                                                                     "startColumnIndex": 0,
                                                                     "endColumnIndex": len(data_to_insert[1])}}}})
        spreadsheet.batch_update({"requests": all_requests})
        logger.info("Данные успешно записаны в Google Таблицу!")
    except Exception as e:
        logger.error(f"Ошибка при подключении или выполнении запроса: {e}")


def write_google_real_cost():
    sheet_name = 'Косты Реальные'
    engine = create_engine(DB_URL)

    query = "SELECT month_date, year_date, vendor_code, cost FROM cost_price ORDER BY year_date desc, month_date desc, vendor_code"

    try:
        all_requests = []
        headers = [
            'Месяц',
            'Год',
            'Артикул',
            'Кост'
        ]

        logger.info("Считываю данные с БД.")
        df = pd.read_sql(query, engine)
        data_to_insert = df.values.tolist()

        logger.info("Подключаюсь к Google Таблице.")
        creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_JSON, SCOPE)
        client = gspread.authorize(creds)
        spreadsheet = client.open('Косты')

        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            logger.info(f"Создаю лист {sheet_name}.")
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=len(headers) + 1)

        logger.info("Очищаю от старых данных.")
        worksheet.delete_rows(1, len(worksheet.get_all_values()))
        logger.info("Начинаю запись.")
        worksheet.insert_row(headers, 1)
        worksheet.insert_rows(data_to_insert, 2)
        logger.info("Применяю стили.")
        all_requests.append({"repeatCell": {"range": {"sheetId": worksheet.id,
                                                      "startRowIndex": 0,
                                                      "endRowIndex": 1,
                                                      "endColumnIndex": len(data_to_insert[1])},
                                            "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER",
                                                                           "verticalAlignment": "MIDDLE",
                                                                           "wrapStrategy": "WRAP"}},
                                            "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment, "
                                                      "wrapStrategy)"}})

        all_requests.append({"addBanding": {"bandedRange": {"range": {"sheetId": worksheet.id,
                                                                      "startRowIndex": 0,
                                                                      "endRowIndex": len(data_to_insert) + 1,
                                                                      "startColumnIndex": 0,
                                                                      "endColumnIndex": len(data_to_insert[0])},
                                                            "rowProperties": {"headerColor": HEADER_COLOR,
                                                                              "firstBandColor": FIRST_BAND_COLOR,
                                                                              "secondBandColor": SECOND_BAND_COLOR}}}})

        all_requests.append({"updateDimensionProperties": {"range": {"sheetId": worksheet.id,
                                                                     "dimension": "COLUMNS",
                                                                     "startIndex": 2,
                                                                     "endIndex": 3},
                                                           "properties": {"pixelSize": 300},
                                                           "fields": "pixelSize"}})

        all_requests.append({"setBasicFilter": {"filter": {"range": {"sheetId": worksheet.id,
                                                                     "startRowIndex": 0,
                                                                     "endRowIndex": len(data_to_insert) + 1,
                                                                     "startColumnIndex": 0,
                                                                     "endColumnIndex": len(data_to_insert[1])}}}})
        spreadsheet.batch_update({"requests": all_requests})
        logger.info("Данные успешно записаны в Google Таблицу!")
    except Exception as e:
        logger.error(f"Ошибка при подключении или выполнении запроса: {e}")


try:
    cost_price()
    write_google_accounting_cost()
    write_google_real_cost()
except Exception as e:
    logger.error(str(e))
