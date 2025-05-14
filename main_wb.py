import asyncio
import logging

import nest_asyncio

from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import OperationalError

from wb_sdk.errors import ClientError
from wb_sdk.wb_api import WBApi
from database import WBDbConnection
from data_classes import DataOperation

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def add_wb_main_entry(db_conn: WBDbConnection, client_id: str, api_key: str) -> None:
    """
        Добавление записей в таблицу `wb_main_table`.

        Args:
            db_conn (WBDbConnection): Объект соединения с базой данных.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
    """
    date = datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start = date - timedelta(days=10)
    end = date - timedelta(microseconds=1)
    logger.info(f"За период с <{start}> до <{end}>")

    list_operation = []

    # Инициализация API-клиента WB
    api_user = WBApi(api_key=api_key)

    # Получение списка продаж
    answer_sales = await api_user.get_supplier_sales(date_from=start.isoformat(), flag=0)

    # Обработка полученных результатов
    for operation in answer_sales.result:
        # Извлечение информации о доставке и отправлении
        accrual_date = operation.date.date()  # Дата принятия учёта
        if accrual_date > end.date():
            continue
        posting_number = operation.srid   # Уникальный идентификатор заказа
        vendor_code = operation.supplierArticle  # Артикул продукта
        sku = str(operation.nmId)  # Артикул продукта внутри системы WB
        sale = round(float(operation.priceWithDisc), 2)  # Стоимость продажи товара
        commission = round(float(sale - operation.forPay), 2)  # Комиссия
        if sale > 0:
            type_of_transaction = "delivered"
            quantities = 1
        else:
            type_of_transaction = "cancelled"
            quantities = -1

        list_operation.append(DataOperation(client_id=client_id,
                                            accrual_date=accrual_date,
                                            type_of_transaction=type_of_transaction,
                                            vendor_code=vendor_code,
                                            delivery_schema="-",
                                            posting_number=posting_number,
                                            sku=sku,
                                            sale=sale,
                                            quantities=quantities,
                                            commission=commission))

    logger.info(f"Количество записей: {len(list_operation)}")
    db_conn.add_wb_operation(list_operations=list_operation)


async def main_func_wb(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()
        db_conn.start_db()

        clients = db_conn.get_clients(marketplace="WB")

        for client in clients:
            try:
                logger.info(f"Добавление в базу данных компании '{client.name_company}'")
                await add_wb_main_entry(db_conn=db_conn, client_id=client.client_id, api_key=client.api_key)
            except ClientError as e:
                logger.error(f'{e}')
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
