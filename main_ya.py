import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import OperationalError

from classes import DataOperation
from ya_sdk.ya_api import YandexApi
from database import YaDbConnection

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def get_orders(api_key: str, updated_at_from: str, updated_at_to: str, page: int = 1) -> list[int]:
    list_orders = []
    api_user = YandexApi(api_key=api_key)
    answer_orders = await api_user.get_campaigns_orders(updated_at_from=updated_at_from,
                                                        updated_at_to=updated_at_to,
                                                        status=['DELIVERED'],
                                                        page=page)
    if answer_orders:
        for order in answer_orders.orders:
            list_orders.append(order.id_field)

    if answer_orders.pager.pagesCount > page:
        extend_orders = await get_orders(api_key=api_key,
                                         updated_at_from=updated_at_from,
                                         updated_at_to=updated_at_to,
                                         page=page + 1)
        list_orders.extend(extend_orders)

    return list_orders


async def get_operations(client_id: str, api_key: str, updated_at_from: str, updated_at_to: str, page: int = 1) \
        -> list[DataOperation]:
    """
        Получает список операций для указанного клиента за определенный период времени.

        Args:
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            updated_at_from (str): Начальная дата периода (в формате строки)
                Формат: YYYY-MM-DDTHH:mm:ss.sssZ.
                Пример: 2019-11-25T10:43:06.51Z.
            updated_at_to (str): Конечная дата периода (в формате строки).
                Формат: YYYY-MM-DDTHH:mm:ss.sssZ.
                Пример: 2019-11-25T10:43:06.51Z.
            page (int, optional): Номер страницы результатов запроса.. Default to 1.

        Returns:
            list[DataOperation]: Список операций.
    """
    list_operation = []
    request_date = datetime.strptime(updated_at_from.split('T')[0], '%Y-%m-%d').date()
    date_format = '%Y-%m-%d'

    # Инициализация API-клиента Yandex
    api_user = YandexApi(api_key=api_key)

    # Получение списка заказов
    list_orders = await get_orders(api_key=api_key,
                                   updated_at_from=updated_at_from,
                                   updated_at_to=updated_at_to)

    answer = await api_user.get_campaigns_stats_orders(orders=list_orders, limit=200)
    if answer:
        for order in answer.result.orders:
            posting_number = str(order.id_field)  # Номер отправления
            print(posting_number)
            accrual_date = datetime.strptime(order.statusUpdateDate.split('T')[0], date_format).date()  # Дата доставки
            for pay in order.payments:
                if pay.source == 'MARKETPLACE':
                    payment_date = datetime.strptime(pay.date, date_format).date()
                    print(accrual_date == payment_date)
            for item in order.items:
                vendor_code = item.shopSku
                quantities = item.count
                delivery_schema = item.warehouse.name
                sku = str(item.marketSku)
                sale = round(sum([price.total for price in item.prices]), 2)
                if order.status == 'DELIVERED':
                    type_of_transaction = 'delivered'
                else:
                    type_of_transaction = 'cancelled'
                    sale = -sale
                    quantities = -quantities

                list_operation.append(DataOperation(client_id=client_id,
                                                    accrual_date=accrual_date,
                                                    type_of_transaction=type_of_transaction,
                                                    vendor_code=vendor_code,
                                                    delivery_schema=delivery_schema,
                                                    posting_number=posting_number,
                                                    sku=sku,
                                                    sale=sale,
                                                    quantities=quantities))

    return list_operation


async def add_yandex_main_entry(db_conn: YaDbConnection, client_id: str, api_key: str, date: datetime) -> None:
    """
        Добавление записей в таблицу `ya_main_table` за указанную дату

        Args:
            db_conn (YaDbConnection): Объект соединения с базой данных Azure.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            date (datetime): Дата, для которой добавляются записи.
    """
    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1) - timedelta(microseconds=1)
    logger.info(f"За период с <{start}> до <{end}>")
    operations = await get_operations(client_id=client_id,
                                      api_key=api_key,
                                      updated_at_from=start.isoformat(),
                                      updated_at_to=end.isoformat())
    logger.info(f"Количество записей: {len(operations)}")
    #db_conn.add_ya_operation(client_id=client_id, list_operations=operations)


async def main_func_yandex(retries: int = 6) -> None:
    """
        Основная функция для обновления записей в базе данных.

        Получает список клиентов из базы данных, затем для каждого клиента добавляет записи за вчерашний день в таблицу `ya_main_table`.
    """
    try:
        db_conn = YaDbConnection()
        db_conn.start_db()
        clients = db_conn.get_client(marketplace='Yandex')
        date = datetime(year=2024, month=5, day=17, tzinfo=timezone(timedelta(hours=3)))
        while date.date() == datetime.now().date():
            for client in clients:
                logger.info(f"Добавление в базу данных компании '{client.name_company}'")
                await add_yandex_main_entry(db_conn=db_conn, client_id=client.client_id, api_key=client.api_key, date=date)
            date += timedelta(days=1)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_func_yandex(retries=retries - 1)
    #except Exception as e:
    #    logger.error(f'{e}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_func_yandex())
    loop.stop()
