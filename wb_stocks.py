import asyncio
import logging

import nest_asyncio

from datetime import datetime

from sqlalchemy.exc import OperationalError

from wb_sdk.wb_api import WBApi
from database import WBDbConnection
from data_classes import DataWBStock

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def get_stocks(db_conn: WBDbConnection, client_id: str, api_key: str) -> None:
    """
        Получает список расходов по хранению для указанного клиента за определенный период времени.

        Args:
            db_conn (WBDbConnection): Объект соединения с базой данных.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
    """
    list_stocks = []

    # Инициализация API-клиента WB
    api_user = WBApi(api_key=api_key)

    # Создание отчёта по хранению
    answer = await api_user.get_supplier_stocks(date_from=datetime(year=2000, month=1, day=1).date().isoformat())

    if answer:
        for stock in answer.result:
            if stock.quantity or stock.inWayToClient or stock.inWayFromClient:
                list_stocks.append(DataWBStock(date=datetime.today().date(),
                                               client_id=client_id,
                                               sku=str(stock.nmId),
                                               vendor_code=stock.supplierArticle,
                                               size=stock.techSize,
                                               category=stock.category,
                                               subject=stock.subject,
                                               warehouse=stock.warehouseName,
                                               quantity_warehouse=stock.quantity,
                                               quantity_to_client=stock.inWayToClient,
                                               quantity_from_client=stock.inWayFromClient))

    # Агрегирование данных
    aggregate = {}
    for row in list_stocks:
        key = (
            row.date,
            row.client_id,
            row.sku,
            row.size,
            row.warehouse
        )
        if key in aggregate:
            aggregate[key].append((row.quantity_warehouse,
                                   row.quantity_to_client,
                                   row.quantity_from_client,
                                   row.vendor_code,
                                   row.category,
                                   row.subject))
        else:
            aggregate[key] = [(row.quantity_warehouse,
                               row.quantity_to_client,
                               row.quantity_from_client,
                               row.vendor_code,
                               row.category,
                               row.subject)]

    list_stocks = []
    for key, value in aggregate.items():
        date, client_id, sku, size, warehouse = key
        quantity_warehouse = sum([val[0] for val in value])
        quantity_to_client = sum([val[1] for val in value])
        quantity_from_client = sum([val[2] for val in value])
        vendor_code = value[0][3]
        category = value[0][4]
        subject = value[0][5]
        list_stocks.append(DataWBStock(
            date=date,
            client_id=client_id,
            sku=sku,
            vendor_code=vendor_code,
            size=size,
            category=category,
            subject=subject,
            warehouse=warehouse,
            quantity_warehouse=quantity_warehouse,
            quantity_to_client=quantity_to_client,
            quantity_from_client=quantity_from_client)
        )
    logger.info(f"Количсетво строк: {len(list_stocks)}")
    db_conn.add_wb_stock_entry(list_stocks=list_stocks)


async def main_wb_stock(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()

        db_conn.start_db()

        clients = db_conn.get_clients(marketplace="WB")

        for client in clients:
            logger.info(f'Сбор информации о остатках на складах {client.name_company}')
            await get_stocks(db_conn=db_conn,
                             client_id=client.client_id,
                             api_key=client.api_key)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_wb_stock(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_wb_stock())
    loop.stop()
