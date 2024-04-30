import asyncio
import os
import nest_asyncio

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

from class_operation import Operation
from wb_sdk.wb_api import WBApi
from database import AzureDbConnection, ConnectionSettings

nest_asyncio.apply()
load_dotenv()


async def get_operations(client_id: str, api_key: str, from_date: str) -> list[Operation]:
    """
        Получает список операций для указанного клиента за определенный период времени.

        Args:
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            from_date (str): Начальная дата периода (в формате строки)
                Формат: YYYY-MM-DDTHH:mm:ss.sssZ.
                Пример: 2019-11-25T10:43:06.51Z.

        Returns:
            list[Operation]: Список операций.
    """
    list_operation = []

    # Инициализация API-клиента Ozon
    api_user = WBApi(api_key=api_key)

    # Получение списка продаж
    try:
        answer_sales = await api_user.get_supplier_sales_response(date_from=from_date, flag=0)
    except TypeError:
        await asyncio.sleep(60)
        answer_sales = await api_user.get_supplier_sales_response(date_from=from_date, flag=0)

    # Обработка полученных результатов
    for operation in answer_sales.result:
        if operation.orderType != "Клиентский":
            continue

        # Извлечение информации о доставке и отправлении
        accrual_date = operation.date.date()  # Дата принятия учёта
        posting_number = operation.gNumber   # Номер отправления
        vendor_cod = operation.supplierArticle  # Артикул продукта
        sku = str(operation.nmId)  # Артикул продукта внутри системы WB
        sale = round(float(operation.priceWithDisc), 2)  # Стоимость продажи товара
        if sale > 0:
            type_of_transaction = "delivered"
            quantities = 1
        else:
            type_of_transaction = "cancelled"
            quantities = -1

        # Добавление операции в список
        list_operation.append(Operation(client_id=client_id,
                                        accrual_date=accrual_date,
                                        type_of_transaction=type_of_transaction,
                                        vendor_cod=vendor_cod,
                                        delivery_schema="-",
                                        posting_number=posting_number,
                                        sku=sku,
                                        sale=sale,
                                        quantities=quantities))
    return list_operation


async def add_wb_main_entry(db_conn: AzureDbConnection, client_id: str, api_key: str, date: datetime) -> None:
    """
        Добавление записей в таблицу `wb_main_table` за указанную дату

        Args:
            db_conn (AzureDbConnection): Объект соединения с базой данных Azure.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            date (datetime): Дата, для которой добавляются записи.
    """
    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1) - timedelta(microseconds=1)
    print(f"За период с <{start}> до <{end}>")
    operations = await get_operations(client_id=client_id,
                                      api_key=api_key,
                                      from_date=start.isoformat())
    print(f"Количество записей: {len(operations)}")
    db_conn.add_pack_wb_main_entry(client_id=client_id, list_operations=operations)


async def main_func_wb(retries: int = 6) -> None:
    try:
        conn_settings = ConnectionSettings(server=os.getenv("SERVER"),
                                           database=os.getenv("DATABASE"),
                                           driver=os.getenv("DRIVER"),
                                           username=os.getenv("USER"),
                                           password=os.getenv("PASSWORD"),
                                           timeout=int(os.getenv("LOGIN_TIMEOUT")))
        db_conn = AzureDbConnection(conn_settings=conn_settings)
        clients = db_conn.get_select_client(marketplace="WB")
        for client in clients:
            print(f"Добавление в базу данных компании '{client.name_company}'")
            date = datetime.now(tz=timezone.utc) - timedelta(days=1)
            await add_wb_main_entry(db_conn=db_conn, client_id=client.client_id, api_key=client.api_key, date=date)
    except OperationalError as e:
        print(f'{e}', datetime.now().isoformat())
        if retries > 0:
            await asyncio.sleep(10)
            await main_func_wb(retries=retries - 1)
    except Exception as e:
        print(f'{e}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_func_wb())
    loop.stop()
