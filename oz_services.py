import asyncio
import logging

import nest_asyncio

from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import OperationalError

from database import OzDbConnection
from ozon_sdk.ozon_api import OzonApi
from data_classes import DataOzService
from ozon_sdk.errors import ClientError

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def add_oz_services(db_conn: OzDbConnection, client_id: str, api_key: str, date_now: datetime) -> None:
    """
        Добавление записей в таблицу `oz_services` за указанную дату.

        Args:
            db_conn (OzDbConnection): Объект соединения с базой данных.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
            date_now (datetime): Начальная дата периода.
    """
    start = date_now - timedelta(days=2)
    end = date_now - timedelta(microseconds=1)
    logger.info(f"За период с <{start}> до <{end}>")

    page = 1
    list_services = []

    # Инициализация API-клиента Ozon
    api_user = OzonApi(client_id=client_id, api_key=api_key)
    while True:
        # Получение списка финансовых транзакций
        answer = await api_user.get_finance_transaction_list(from_field=start.isoformat(),
                                                             to=end.isoformat(),
                                                             page=page)

        # Обработка полученных результатов
        for operation in answer.result.operations:
            percentage_of_sales = {}
            vendor = {}

            delivery_schema = operation.posting.delivery_schema
            accruals_for_sale = operation.accruals_for_sale

            accrual_date = operation.operation_date.date()
            operation_type = operation.operation_type
            operation_type_name = operation.operation_type_name
            posting_number = operation.posting.posting_number

            skus = [str(item.sku) for item in operation.items]

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

                products = answer_fb.result.products
                if not accruals_for_sale:
                    accruals_for_sale = sum([float(product.price) * product.quantity for product in products])
                for product in products:
                    sale = float(product.price)
                    percentage = sale / accruals_for_sale
                    percentage_of_sales[str(product.sku)] = percentage
                    vendor[str(product.sku)] = product.offer_id

            for service in operation.services:
                service_name = service.name
                total_cost = round(service.price, 2)

                if len(skus) > 1:
                    for sku in skus:
                        if percentage_of_sales.get(sku):
                            cost = round(total_cost * percentage_of_sales.get(sku), 2)
                        else:
                            cost = round(total_cost / len(skus), 2)
                        list_services.append(DataOzService(client_id=client_id,
                                                           date=accrual_date,
                                                           operation_type=operation_type,
                                                           operation_type_name=operation_type_name or None,
                                                           vendor_code=vendor.get(sku),
                                                           sku=sku,
                                                           posting_number=posting_number or None,
                                                           service=service_name,
                                                           cost=cost))
                else:
                    if skus:
                        vendor_code = vendor.get(skus[0])
                    else:
                        vendor_code = None
                    list_services.append(DataOzService(client_id=client_id,
                                                       date=accrual_date,
                                                       operation_type=operation_type,
                                                       operation_type_name=operation_type_name or None,
                                                       vendor_code=vendor_code,
                                                       sku=', '.join(skus) or None,
                                                       posting_number=posting_number or None,
                                                       service=service_name or None,
                                                       cost=total_cost))

            if not len(operation.services) and operation_type not in ['ClientReturnAgentOperation',
                                                                      'OperationAgentDeliveredToCustomer']:
                cost = round(operation.amount, 2)
                list_services.append(DataOzService(client_id=client_id,
                                                   date=accrual_date,
                                                   operation_type=operation_type,
                                                   operation_type_name=operation_type_name or None,
                                                   vendor_code=None,
                                                   sku=', '.join(skus) or None,
                                                   posting_number=posting_number or None,
                                                   service=None,
                                                   cost=cost))

        # Получение дополнительных страниц результатов
        if page >= answer.result.page_count:
            break

        page += 1

    # Агрегирование данных
    aggregate = {}
    for row in list_services:
        key = (
            row.client_id,
            row.date,
            row.operation_type,
            row.operation_type_name,
            row.vendor_code,
            row.sku,
            row.posting_number,
            row.service
        )
        if key in aggregate:
            aggregate[key] += row.cost
        else:
            aggregate[key] = row.cost
    list_services = []
    for key, cost in aggregate.items():
        client_id, date_now, operation_type, operation_type_name, vendor_code, sku, posting_number, service = key
        list_services.append(DataOzService(client_id=client_id,
                                           date=date_now,
                                           operation_type=operation_type,
                                           operation_type_name=operation_type_name,
                                           vendor_code=vendor_code,
                                           sku=sku,
                                           posting_number=posting_number,
                                           service=service,
                                           cost=cost))

    logger.info(f'Количество записей: {len(list_services)}')
    db_conn.add_oz_services_entry(client_id=client_id, list_services=list_services)


async def main_oz_services(retries: int = 6) -> None:
    try:
        db_conn = OzDbConnection()

        db_conn.start_db()

        clients = db_conn.get_clients(marketplace="Ozon")

        date_now = datetime.now(tz=timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        for client in clients:
            try:
                logger.info(f"Добавление в базу данных компании '{client.name_company}'")
                await add_oz_services(db_conn=db_conn,
                                      client_id=client.client_id,
                                      api_key=client.api_key,
                                      date_now=date_now)
            except ClientError as e:
                logger.error(f'{e}')
                continue
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_oz_services(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_oz_services())
    loop.stop()
