import os
import gspread
import logging
import datetime
import warnings

from sqlalchemy import create_engine, text
from oauth2client.service_account import ServiceAccountCredentials

from config import DB_URL

warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
PATH_JSON = os.path.join(PROJECT_ROOT, 'templates', 'service-account-432709-1178152e9e49.json')
PROJECT = 'Расчет себестоимости'

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

column = ['month_date', 'year_date', 'vendor_code', 'cost']


def get_values(to_date: datetime.date) -> list:
    creds = ServiceAccountCredentials.from_json_keyfile_name(PATH_JSON, SCOPE)
    client = gspread.authorize(creds)
    spreadsheet = client.open(PROJECT)

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
            vendor_code = row[0].lower()
            cost = round(float(row[14].replace(',', '.') or row[1].replace(',', '.')), 2)
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


try:
    cost_price()
except Exception as e:
    logger.error(str(e))
