import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import OperationalError

from data_classes import DataYaOrder, DataYaCampaigns
from ya_sdk.ya_api import YandexApi
from database import YaDbConnection

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def get_campaign_ids(api_key: str) -> list[DataYaCampaigns]:
    list_campaigns = []
    api_user = YandexApi(api_key=api_key)
    answer = await api_user.get_campaigns()
    if answer:
        for campaign in answer.campaigns:
            list_campaigns.append(DataYaCampaigns(client_id=str(campaign.business.field_id),
                                                  campaign_id=str(campaign.field_id),
                                                  name=campaign.domain,
                                                  placement_type=campaign.placementType))
    return list_campaigns


async def get_orders(api_key: str, campaign_id: str, updated_at_from: str, updated_at_to: str) -> list[int]:
    list_orders = []
    page = 1

    api_user = YandexApi(api_key=api_key)
    while True:
        answer_orders = await api_user.get_campaigns_orders(campaign_id=campaign_id,
                                                            updated_at_from=updated_at_from,
                                                            updated_at_to=updated_at_to,
                                                            status=[],
                                                            page=page)
        if answer_orders:
            for order in answer_orders.orders:
                list_orders.append(order.id_field)

        if answer_orders.pager.pagesCount <= page:
            break

        page += 1

    return list_orders


async def add_yandex_orders_entry(db_conn: YaDbConnection, client_id: str, campaign_id: str, api_key: str,
                                  date_now: datetime) -> None:
    """
        Получает список операций для указанного клиента за определенный период времени.

        Args:
            db_conn (YaDbConnection): Объект соединения с базой данных.
            client_id (str): ID кабинета.
            campaign_id (str): ID магазина.
            api_key (str): API KEY кабинета.
            date_now (datetime): Дата.
    """
    start = date_now - timedelta(days=1)
    end = datetime.now(tz=timezone(timedelta(hours=3)))

    logger.info(f"За период с <{start}> до <{end}>")

    list_operation = []
    date_format = '%Y-%m-%d'

    # Инициализация API-клиента Yandex
    api_user = YandexApi(api_key=api_key)

    # Получение списка заказов
    list_orders = await get_orders(campaign_id=campaign_id,
                                   api_key=api_key,
                                   updated_at_from=start.isoformat(),
                                   updated_at_to=end.isoformat())
    if not list_orders:
        return

    page_token = None

    while True:
        answer = await api_user.get_campaigns_stats_orders(campaign_id=campaign_id,
                                                           orders=list_orders,
                                                           limit=200,
                                                           page_token=page_token)
        if not answer.result:
            break

        for order in answer.result.orders:
            posting_number = str(order.id_field)  # Номер отправления
            order_date = datetime.strptime(order.creationDate, date_format).date()  # Дата заказа
            if order_date == date_now.date() or order_date < datetime(year=2024, month=6, day=1).date():
                continue
            update_date = datetime.strptime(order.statusUpdateDate.split('T')[0], date_format).date()  # Дата обновления
            for item in order.items:
                vendor_code = item.shopSku
                quantities = item.count
                rejected = sum([detail.itemCount for detail in item.details if detail.itemStatus == 'REJECTED'])
                returned = sum([detail.itemCount for detail in item.details if detail.itemStatus == 'RETURNED'])
                sku = str(item.marketSku)
                price = round(sum([price.total for price in item.prices]) / quantities, 2)
                list_operation.append(DataYaOrder(client_id=client_id,
                                                  order_date=order_date,
                                                  sku=sku,
                                                  vendor_code=vendor_code,
                                                  posting_number=posting_number,
                                                  delivery_schema=campaign_id,
                                                  price=price,
                                                  quantities=quantities,
                                                  rejected=rejected,
                                                  returned=returned,
                                                  status=order.status,
                                                  update_date=update_date))

        if not answer.result.paging.nextPageToken:
            break

        page_token = answer.result.paging.nextPageToken

    logger.info(f"Количество записей: {len(list_operation)}")
    db_conn.add_ya_orders(list_orders=list_operation)


async def main_orders_yandex(retries: int = 6) -> None:
    """
        Основная функция для обновления записей в базе данных.

        Получает список клиентов из базы данных,
        затем для каждого клиента добавляет записи за вчерашний день в таблицу `ya_main_table`.
    """
    try:
        db_conn = YaDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace='Yandex')
        api_key_set = {client.api_key for client in clients}
        for api_key in api_key_set:
            list_campaigns = await get_campaign_ids(api_key=api_key)
            db_conn.add_ya_campaigns(list_campaigns=list_campaigns)

            date_now = datetime.now(tz=timezone(timedelta(hours=3))).replace(hour=0, minute=0, second=0, microsecond=0)

            for campaign in sorted(list_campaigns, key=lambda x: x.client_id):
                client = db_conn.get_client(client_id=campaign.client_id)
                logger.info(f"Добавление в базу данных компании '{client.name_company}' магазина '{campaign.name}'")
                await add_yandex_orders_entry(db_conn=db_conn,
                                              client_id=client.client_id,
                                              campaign_id=campaign.campaign_id,
                                              api_key=client.api_key,
                                              date_now=date_now)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_orders_yandex(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_orders_yandex())
    loop.stop()
