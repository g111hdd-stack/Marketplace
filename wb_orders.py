import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import OperationalError

from data_classes import DataOrder
from wb_sdk.wb_api import WBApi
from database import WBDbConnection

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def get_orders(client_id: str, api_key: str, from_date: str) -> list[DataOrder]:
    """
        Получает список заказов для указанного клиента за определенный период времени.

        Args:
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            from_date (str): Начальная дата периода (в формате строки)
                Формат: YYYY-MM-DDTHH:mm:ss.sssZ.
                Пример: 2019-11-25T10:43:06.51Z.

        Returns:
            list[DataOrder]: Список заказов.
    """
    list_orders = []

    # Инициализация API-клиента Ozon
    api_user = WBApi(api_key=api_key)

    # Получение списка заказов
    answer_orders = await api_user.get_supplier_orders_response(date_from=from_date, flag=1)

    # Обработка полученных результатов
    for order in answer_orders.result:
        if order.orderType != "Клиентский":
            continue

        order_date = order.date.date()  # Дата заказа
        posting_number = order.srid   # Уникальный идентификатор заказа
        vendor_code = order.supplierArticle  # Артикул продукта
        sku = str(order.nmId)  # Артикул продукта внутри системы WB
        price = round(float(order.priceWithDisc), 2)  # Стоимость продажи товара

        # Добавление заказа в список
        list_orders.append(DataOrder(client_id=client_id,
                                     order_date=order_date,
                                     sku=sku,
                                     vendor_code=vendor_code,
                                     category=order.category,
                                     subject=order.subject,
                                     posting_number=posting_number,
                                     price=price))
    return list_orders


async def add_wb_orders_entry(db_conn: WBDbConnection, client_id: str, api_key: str, date: datetime) -> None:
    """
        Добавление записей в таблицу `wb_orders_table` за указанную дату

        Args:
            db_conn (WBDbConnection): Объект соединения с базой данных Azure.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            date (datetime): Дата, для которой добавляются записи.
    """
    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1) - timedelta(microseconds=1)
    logger.info(f"За период с <{start}> до <{end}>")
    orders = await get_orders(client_id=client_id,
                              api_key=api_key,
                              from_date=start.date().isoformat())
    logger.info(f"Количество записей: {len(orders)}")
    db_conn.add_wb_orders(client_id=client_id, list_orders=orders)


async def main_orders_wb(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace="WB")
        date = datetime.now(tz=timezone(timedelta(hours=3))) - timedelta(days=1)
        for client in clients:
            logger.info(f"Добавление в базу данных компании '{client.name_company}'")
            await add_wb_orders_entry(db_conn=db_conn, client_id=client.client_id, api_key=client.api_key, date=date)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_orders_wb(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_orders_wb())
    loop.stop()
