import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import OperationalError

from data_classes import DataOperation
from wb_sdk.wb_api import WBApi
from database import WBDbConnection

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def get_operations(client_id: str, api_key: str, from_date: str) -> list[DataOperation]:
    """
        Получает список операций для указанного клиента за определенный период времени.

        Args:
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            from_date (str): Начальная дата периода (в формате строки)
                Формат: YYYY-MM-DDTHH:mm:ss.sssZ.
                Пример: 2019-11-25T10:43:06.51Z.

        Returns:
            list[DataOperation]: Список операций.
    """
    list_operation = []

    # Инициализация API-клиента Ozon
    api_user = WBApi(api_key=api_key)

    # Получение списка продаж
    answer_sales = await api_user.get_supplier_sales_response(date_from=from_date, flag=1)

    # Обработка полученных результатов
    for operation in answer_sales.result:
        if operation.orderType != "Клиентский":
            continue

        # Извлечение информации о доставке и отправлении
        accrual_date = operation.date.date()  # Дата принятия учёта
        posting_number = operation.srid   # Уникальный идентификатор заказа
        vendor_code = operation.supplierArticle  # Артикул продукта
        sku = str(operation.nmId)  # Артикул продукта внутри системы WB
        sale = round(float(operation.priceWithDisc), 2)  # Стоимость продажи товара
        if sale > 0:
            type_of_transaction = "delivered"
            quantities = 1
        else:
            type_of_transaction = "cancelled"
            quantities = -1

        # Добавление операции в список
        list_operation.append(DataOperation(client_id=client_id,
                                            accrual_date=accrual_date,
                                            type_of_transaction=type_of_transaction,
                                            vendor_code=vendor_code,
                                            delivery_schema="-",
                                            posting_number=posting_number,
                                            sku=sku,
                                            sale=sale,
                                            quantities=quantities))
    return list_operation


async def add_wb_main_entry(db_conn: WBDbConnection, client_id: str, api_key: str, date: datetime) -> None:
    """
        Добавление записей в таблицу `wb_main_table` за указанную дату

        Args:
            db_conn (WBDbConnection): Объект соединения с базой данных Azure.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            date (datetime): Дата, для которой добавляются записи.
    """
    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1) - timedelta(microseconds=1)
    logger.info(f"За период с <{start}> до <{end}>")
    operations = await get_operations(client_id=client_id,
                                      api_key=api_key,
                                      from_date=start.isoformat())
    logger.info(f"Количество записей: {len(operations)}")
    db_conn.add_wb_operation(client_id=client_id, list_operations=operations)


async def main_func_wb(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace="WB")
        date = datetime.now(tz=timezone.utc) - timedelta(days=1)
        for client in clients:
            logger.info(f"Добавление в базу данных компании '{client.name_company}'")
            await add_wb_main_entry(db_conn=db_conn, client_id=client.client_id, api_key=client.api_key, date=date)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_func_wb(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_func_wb())
    loop.stop()
