import asyncio
import logging

import nest_asyncio

from datetime import timedelta, datetime, date

from sqlalchemy.exc import OperationalError

from wb_sdk.errors import ClientError
from wb_sdk.wb_api import WBApi
from data_classes import DataWBOrderFBS, DataWBWarehouseFBS, DataWBSupplyFBS, DataWBStockFBS
from database import WBDbConnection

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def add_wb_fbs_warehouses_entry(db_conn: WBDbConnection, client_id: str, api_key: str) -> None:
    """
        Получает список складов FBS для указанного клиента.

        Args:
            db_conn (WBDbConnection): Объект соединения с базой данных.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
    """
    api_user = WBApi(api_key=api_key)
    answer = await api_user.get_fbs_warehouses()

    list_warehouses = []

    for warehouse in answer.result:
        list_warehouses.append(DataWBWarehouseFBS(client_id=client_id,
                                                  warehouse_id=str(warehouse.id_field),
                                                  name=warehouse.name,
                                                  office_id=str(warehouse.officeId),
                                                  cargo_type=warehouse.cargoType,
                                                  delivery_type=warehouse.deliveryType))

    db_conn.add_wb_fbs_warehouses(list_warehouses=list_warehouses)


async def add_wb_fbs_orders_entry(db_conn: WBDbConnection, client_id: str, api_key: str, date_to: datetime) -> None:
    """
        Получает список заказов для указанного клиента за определенный период времени.

        Args:
            db_conn (WBDbConnection): Объект соединения с базой данных.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            date_to (datetime): Конечная дата запрос.
    """
    date_from = date_to.replace(hour=0, minute=0, second=0, microsecond=0)
    logger.info(f"За период от {date_from} до {date_to}")

    list_orders = []
    next_field = 0

    # Инициализация API-клиента WB
    api_user = WBApi(api_key=api_key)

    while True:
        # Получение списка заказов
        answer_orders = await api_user.get_fbs_orders(date_from=date_from,
                                                      date_to=date_to,
                                                      next_field=next_field)

        # Обработка полученных результатов
        for order in answer_orders.orders:
            supply_id = order.supplyId
            warehouse_id = str(order.warehouseId)
            order_date = order.createdAt.replace(tzinfo=None) + timedelta(hours=3)
            posting_number = order.rid
            vendor_code = order.article
            sku = str(order.nmId)
            barcodes = order.skus

            # Добавление заказа в список
            list_orders.append(DataWBOrderFBS(supply_id=supply_id,
                                              client_id=client_id,
                                              warehouse_id=warehouse_id,
                                              order_date=order_date,
                                              posting_number=posting_number,
                                              vendor_code=vendor_code,
                                              sku=sku,
                                              barcodes=barcodes))
        if len(answer_orders.orders) == 1000 and answer_orders.next_field:
            next_field = answer_orders.next_field
            continue
        break

    logger.info(f"Количество записей: {len(list_orders)}")
    db_conn.add_wb_fbs_orders(list_orders=list_orders)


async def add_wb_fbs_supplies_entry(db_conn: WBDbConnection, client_id: str, api_key: str) -> None:
    """
        Получаем данные по поставкам по указанному клиенту.

        Args:
            db_conn (WBDbConnection): Объект соединения с базой данных.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
    """

    list_supplies = []

    # Инициализация API-клиента WB
    api_user = WBApi(api_key=api_key)

    supplies = db_conn.get_fbs_supplies(client_id=client_id)

    for supply_id in supplies:
        answer = await api_user.get_fbs_supply(supply_id=supply_id)

        # Обработка полученных результатов
        done = answer.done
        created_at = answer.createdAt.replace(tzinfo=None) + timedelta(hours=3)

        closed_at = answer.closedAt
        if closed_at:
            closed_at = closed_at.replace(tzinfo=None) + timedelta(hours=3)
        scan_dt = answer.scanDt
        if scan_dt:
            scan_dt = scan_dt.replace(tzinfo=None) + timedelta(hours=3)
        name = answer.name
        cargo_type = answer.cargoType

        list_supplies.append(DataWBSupplyFBS(supply_id=supply_id,
                                             client_id=client_id,
                                             done=done,
                                             created_at=created_at,
                                             closed_at=closed_at,
                                             scan_dt=scan_dt,
                                             name=name,
                                             cargo_type=cargo_type))

    db_conn.add_wb_fbs_supplies(list_supplies=list_supplies)


# async def add_wb_fbs_stock_entry(db_conn: WBDbConnection, client_id: str, api_key: str) -> None:
#     """
#         Получаем данные об остатках на складах FBS по указанному клиенту.
#
#         Args:
#             db_conn (WBDbConnection): Объект соединения с базой данных.
#             client_id (str): ID кабинета.
#             api_key (str): API KEY кабинета.
#     """
#
#     list_stocks = []
#
#     # Инициализация API-клиента WB
#     api_user = WBApi(api_key=api_key)
#
#     warehouse_barcodes = db_conn.get_fbs_barcodes(client_id=client_id)
#
#     for warehouse_id, barcodes in warehouse_barcodes.items():
#         for skus in [barcodes[i:i + 1000] for i in range(0, len(barcodes), 1000)]:
#             sku_to_vendor = dict(skus)
#             answer = await api_user.get_fbs_stocks(warehouse_id=warehouse_id, skus=list(sku_to_vendor.keys()))
#             for stock in answer.stocks:
#                 list_stocks.append(DataWBStockFBS(client_id=client_id,
#                                                   warehouse_id=warehouse_id,
#                                                   date=date.today(),
#                                                   barcode=stock.sku,
#                                                   vendor_code=sku_to_vendor.get(stock.sku, None),
#                                                   count=stock.amount))
#
#     db_conn.add_wb_fbs_stocks(list_stocks=list_stocks)


async def main_fbs_orders_wb(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()
        db_conn.start_db()

        clients = db_conn.get_clients(marketplace="WB")

        date_to = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(microseconds=1)

        for client in clients:
            try:
                logger.info(f"Получаем список складов FBS компании {client.name_company}")
                await add_wb_fbs_warehouses_entry(db_conn=db_conn, client_id=client.client_id, api_key=client.api_key)
            except ClientError as e:
                logger.error(f'{e}')
            try:
                logger.info(f"Добавление в базу данных о заказах FBS компании {client.name_company}")
                await add_wb_fbs_orders_entry(db_conn=db_conn,
                                              client_id=client.client_id,
                                              api_key=client.api_key,
                                              date_to=date_to)
            except ClientError as e:
                logger.error(f'{e}')
            try:
                logger.info(f"Обновляем информацию о поставках FBS компании {client.name_company}")
                await add_wb_fbs_supplies_entry(db_conn=db_conn,
                                                client_id=client.client_id,
                                                api_key=client.api_key)
            except ClientError as e:
                logger.error(f'{e}')
            # try:
            #     logger.info(f"Обновляем информацию об остатках на складах FBS компании {client.name_company}")
            #     await add_wb_fbs_stock_entry(db_conn=db_conn,
            #                                  client_id=client.client_id,
            #                                  api_key=client.api_key)
            # except ClientError as e:
            #     logger.error(f'{e}')
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_fbs_orders_wb(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_fbs_orders_wb())
    loop.stop()
