import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta, timezone, tzinfo
from sqlalchemy.exc import OperationalError

from data_classes import DataOperation, DataSbOrders
from sb_sdk.sb_api import SberApi
from database import SbDbConnection


nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def get_shipments(db_conn: SbDbConnection, client_id: str, api_key: str, date_from: str, date_to: str) -> list[str]:
    list_shipments = db_conn.get_not_delivered_orders(client_id=client_id)
    statuses = db_conn.get_status_orders()
    api_user = SberApi(client_id=client_id, api_key=api_key)
    answer = await api_user.get_order_service_order_search(date_from=date_from,
                                                           date_to=date_to,
                                                           statuses=statuses,
                                                           count=1000)
    if answer:
        if answer.data:
            list_shipments.extend(answer.data.shipments)
    return list_shipments


async def add_operations(db_conn: SbDbConnection, client_id: str, api_key: str, list_shipments: list[str]):
    def format_date(date_format: str) -> datetime.date:
        time_format = "%Y-%m-%d"
        return datetime.strptime(date_format.split('T')[0], time_format).date()

    list_orders = []
    list_delivered = []

    if not list_shipments:
        return

    api_user = SberApi(client_id=client_id, api_key=api_key)
    answer = await api_user.get_order_service_orders(shipments=list_shipments)
    if answer:
        if answer.data:
            for shipment in answer.data.shipments:
                if shipment.status == 'DELIVERED':
                    for item in shipment.items:
                        list_delivered.append(DataOperation(accrual_date=format_date(date_format=shipment.deliveryDate),
                                                            client_id=client_id,
                                                            type_of_transaction='delivered',
                                                            vendor_code=item.offerId,
                                                            posting_number=shipment.shipmentId,
                                                            delivery_schema='-',
                                                            sku=item.goodsId,
                                                            sale=round(float(item.price), 2),
                                                            quantities=item.quantity))

                list_orders.append(DataSbOrders(posting_number=shipment.shipmentId,
                                                client_id=client_id,
                                                field_status=shipment.status,
                                                date_order=format_date(date_format=shipment.creationDate)))

    logger.info(f"Добавление в базу данных выполненых заказов в количестве {len(list_delivered)}")
    db_conn.add_sb_operation(client_id=client_id, list_operations=list_delivered)
    logger.info(f"Обновление информации о заказах")
    db_conn.add_sb_orders(client_id=client_id, list_operations=list_orders)
    db_conn.delete_order_canceled(client_id=client_id)


async def main_func_sb(retries: int = 6) -> None:
    try:
        db_conn = SbDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace="СБЕР")
        date_now = datetime.now(tz=timezone(timedelta(hours=3))).replace(hour=0, minute=0, second=0, microsecond=0)
        date_from = date_now - timedelta(days=1)
        date_to = date_now - timedelta(microseconds=1)

        for client in clients:
            list_shipments = await get_shipments(db_conn=db_conn,
                                                 client_id=client.client_id,
                                                 api_key=client.api_key,
                                                 date_from=date_from.isoformat(),
                                                 date_to=date_to.isoformat())

            logger.info(f"Добавление в базу данных компании '{client.name_company}'")
            await add_operations(db_conn=db_conn,
                                 client_id=client.client_id,
                                 api_key=client.api_key,
                                 list_shipments=list_shipments)

    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_func_sb(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_func_sb())
    loop.stop()
