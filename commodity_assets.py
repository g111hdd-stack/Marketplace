import re
import time
import logging

from datetime import datetime, date, timedelta, timezone

from sqlalchemy.exc import OperationalError

from database import DbConnection
from data_classes import DataSupply, DataCommodityAsset

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)



def add_fbs_stocks(db_conn: DbConnection) -> None:
    list_assets = []
    list_supplies = []

    vendors = db_conn.get_vendors()

    today = date.today()
    pattern = re.compile(r"^\d{2}\.\d{2}\.\d{4}$")

    sheet_names = []

    dates_sheet_names = []
    for name in sheet_names:
        name = name.strip()
        if pattern.match(name):
            try:
                # пытаемся распарсить дату, проверяя её корректность
                date_obj = datetime.strptime(name, "%d.%m.%Y").date()
                dates_sheet_names.append(date_obj)
            except ValueError:
                # если дата некорректная (например, 32.12.2024) — пропускаем
                pass

    latest = max(dates_sheet_names)

    # сравниваем недели (isocalendar возвращает кортеж: (год, номер_недели, день_недели))
    if not ((latest.isocalendar()[0] == today.isocalendar()[0]) and (latest.isocalendar()[1] == today.isocalendar()[1])):
        raise Exception("Invalid date")

    name_list = latest.isoformat()

    # db_conn.add_commodity_assets(list_assets=list_assets)
    # db_conn.add_supplies(list_supplies=list_supplies)

def main_fbs_stocks(retries: int = 6) -> None:
    try:
        db_conn = DbConnection()
        db_conn.start_db()

        add_fbs_stocks(db_conn=db_conn)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            time.sleep(10)
            main_fbs_stocks(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')

if __name__ == "__main__":
    main_fbs_stocks()
