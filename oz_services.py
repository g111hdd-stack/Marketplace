import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import OperationalError

from data_classes import DataOzService
from ozon_sdk.ozon_api import OzonApi
from database import OzDbConnection


nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def get_operations(client_id: str, api_key: str, from_date: str, to_date: str, page: int = 1) \
        -> list[DataOzService]:

    list_services = []

    # Инициализация API-клиента Ozon
    api_user = OzonApi(client_id=client_id, api_key=api_key)

    # Получение списка финансовых транзакций
    answer_transaction = await api_user.get_finance_transaction_list(from_field=from_date,
                                                                     to=to_date,
                                                                     page=page)

    # Обработка полученных результатов
    if answer_transaction.result:
        for operation in answer_transaction.result.operations:
            skus = []
            percentage_of_sales = {}
            vendor = {}

            delivery_schema = operation.posting.delivery_schema
            accruals_for_sale = operation.accruals_for_sale

            accrual_date = operation.operation_date.date()
            operation_type = operation.operation_type
            operation_type_name = operation.operation_type_name
            posting_number = operation.posting.posting_number

            for item in operation.items:
                skus.append(str(item.sku))

            if operation_type in ['OperationAgentDeliveredToCustomer',
                                  'OperationItemReturn',
                                  'OperationReturnGoodsFBSofRMS'] and len(skus) > 1:
                if delivery_schema == 'FBO':
                    answer_fb = await api_user.get_posting_fbo(posting_number=posting_number,
                                                               analytics_data=True,
                                                               financial_data=True,
                                                               translit=True)
                elif delivery_schema in ['FBS', 'RFBS']:
                    answer_fb = await api_user.get_posting_fbs(posting_number=posting_number,
                                                               analytics_data=True,
                                                               financial_data=True,
                                                               translit=True)
                else:
                    continue
                if not accruals_for_sale:
                    accruals_for_sale = sum([float(product.price) * product.quantity for product in answer_fb.result.products])
                for product in answer_fb.result.products:
                    sale = float(product.price)
                    percentage = sale / accruals_for_sale
                    percentage_of_sales[str(product.sku)] = percentage
                    vendor[str(product.sku)] = product.offer_id

            for service in operation.services:
                service_name = service.name
                total_cost = round(float(service.price), 2)

                if len(skus) > 1:
                    for sku in skus:
                        if percentage_of_sales.get(sku):
                            cost = round(total_cost * percentage_of_sales.get(sku), 2)
                        else:
                            cost = round(total_cost / len(skus), 2)
                        list_services.append(DataOzService(client_id=client_id,
                                                           date=accrual_date,
                                                           operation_type=operation_type,
                                                           cost=cost,
                                                           operation_type_name=operation_type_name or None,
                                                           sku=sku,
                                                           posting_number=posting_number or None,
                                                           service=service_name,
                                                           vendor_code=vendor.get(str(sku), None)))
                else:
                    if skus:
                        vendor_code = vendor.get(str(skus[0]), None)
                    else:
                        vendor_code = None
                    list_services.append(DataOzService(client_id=client_id,
                                                       date=accrual_date,
                                                       operation_type=operation_type,
                                                       cost=total_cost,
                                                       operation_type_name=operation_type_name or None,
                                                       sku=', '.join(skus) or None,
                                                       posting_number=posting_number or None,
                                                       service=service_name or None,
                                                       vendor_code=vendor_code))

            if not len(operation.services) and operation_type not in ['ClientReturnAgentOperation',
                                                                      'OperationAgentDeliveredToCustomer']:
                cost = round(float(operation.amount), 2)
                list_services.append(DataOzService(client_id=client_id,
                                                   date=accrual_date,
                                                   operation_type=operation_type,
                                                   cost=cost,
                                                   operation_type_name=operation_type_name or None,
                                                   sku=', '.join(skus) or None,
                                                   posting_number=posting_number or None))

        # Рекурсивный вызов функции для получения дополнительных страниц результатов
        if answer_transaction.result.page_count > page:
            extend_services = await get_operations(client_id=client_id,
                                                   api_key=api_key,
                                                   from_date=from_date,
                                                   to_date=to_date,
                                                   page=page + 1)
            list_services.extend(extend_services)

    return list_services


async def add_oz_main_entry(db_conn: OzDbConnection, client_id: str, api_key: str, date: datetime) -> None:
    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1) - timedelta(microseconds=1)
    # for i in [3, 4, 5, 6, 7, 8]:
    #     start = datetime(year=2024, month=i, day=1, tzinfo=timezone.utc)
    #     end = datetime(year=2024, month=i+1, day=1, tzinfo=timezone.utc) - timedelta(microseconds=1)
    #     if i == 8:
    #         end = datetime(year=2024, month=i, day=8, tzinfo=timezone.utc) - timedelta(microseconds=1)
    logger.info(f"За период с <{start}> до <{end}>")
    services = await get_operations(client_id=client_id,
                                    api_key=api_key,
                                    from_date=start.isoformat(),
                                    to_date=end.isoformat())
    logger.info(f'Количество записей: {len(services)}')
    db_conn.add_oz_services_entry(client_id=client_id, list_services=services)


async def main_func_oz(retries: int = 6) -> None:
    try:
        db_conn = OzDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace="Ozon")
        date = datetime.now(tz=timezone.utc) - timedelta(days=1)
        for client in clients:
            logger.info(f"Добавление в базу данных компании '{client.name_company}'")
            await add_oz_main_entry(db_conn=db_conn, client_id=client.client_id, api_key=client.api_key, date=date)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_func_oz(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_func_oz())
    loop.stop()
