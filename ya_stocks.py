import asyncio
import logging

import nest_asyncio

from datetime import datetime

from sqlalchemy.exc import OperationalError

from ya_sdk.errors import ClientError
from ya_sdk.ya_api import YandexApi
from database import YaDbConnection
from data_classes import DataYaCampaigns, DataYaStock

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


async def get_warehouses(api_key: str) -> dict:
    warehouses = {}
    api_user = YandexApi(api_key=api_key)
    answer = await api_user.get_warehouses()
    if answer:
        for warehouse in answer.result.warehouses:
            warehouses[warehouse.id_field] = warehouse.name
    return warehouses


async def get_stocks(db_conn: YaDbConnection, client_id: str, campaign_id: str, api_key: str, warehouses: dict) -> None:
    list_stocks = []

    # Инициализация API-клиента Yandex
    api_user = YandexApi(api_key=api_key)

    for archived in [True, False]:
        page_token = None
        while True:
            answer = await api_user.get_campaigns_offers_stocks(campaign_id=campaign_id,
                                                                archived=archived,
                                                                page_token=page_token,
                                                                limit=100)
            if not answer.result:
                break

            for warehouse in answer.result.warehouses:
                warehouse_name = warehouses.get(warehouse.warehouseId)
                if warehouse_name is None:
                    continue
                for item in warehouse.offers:
                    vendor_code = item.offerId
                    size = '0'
                    for s in ['/xs', '/s', '/m', '/м', '/l', '/xl', '/2xl']:
                        if vendor_code.lower().endswith(s):
                            size = vendor_code.split('/')[-1].upper()
                            vendor_code = '/'.join(vendor_code.split('/')[:-1])
                            break
                    for stock in item.stocks:
                        list_stocks.append(DataYaStock(date=datetime.today().date(),
                                                       client_id=client_id,
                                                       campaign_id=campaign_id,
                                                       vendor_code=vendor_code,
                                                       size=size,
                                                       warehouse=warehouse_name,
                                                       quantity=stock.count,
                                                       type=stock.type))
            if not answer.result.paging.nextPageToken:
                break

            page_token = answer.result.paging.nextPageToken

    logger.info(f"Количество записей: {len(list_stocks)}")
    db_conn.add_ya_stock_entry(list_stocks=list_stocks)


async def main_wb_stock(retries: int = 6) -> None:
    try:
        db_conn = YaDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace='Yandex')
        api_key_set = {client.api_key for client in clients}

        warehouses = await get_warehouses(list(api_key_set)[0])

        for api_key in api_key_set:
            list_campaigns = await get_campaign_ids(api_key=api_key)
            db_conn.add_ya_campaigns(list_campaigns=list_campaigns)

            for campaign in sorted(list_campaigns, key=lambda x: x.client_id):
                client = db_conn.get_client(client_id=campaign.client_id)
                logger.info(f"Добавление в базу данных компании '{client.name_company}' магазина '{campaign.name}'")
                try:
                    await get_stocks(db_conn=db_conn,
                                     client_id=client.client_id,
                                     campaign_id=campaign.campaign_id,
                                     api_key=client.api_key,
                                     warehouses=warehouses)
                except ClientError as e:
                    logger.error(f'{e}')
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_wb_stock(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_wb_stock())
    loop.stop()
