import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError

from classes import DataOzProductCard
from ozon_sdk.ozon_api import OzonApi, OzonPerformanceAPI
from database import AzureDbConnection

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def get_products_ids(client_id: str, api_key: str) -> list[int]:
    list_product_ids = []
    api_user = OzonApi(client_id=client_id, api_key=api_key)
    last_id = None
    total = 1000
    while total >= 1000:
        answer = await api_user.get_product_list(limit=1000, last_id=last_id)
        if answer:
            if answer.result:
                for item in answer.result.items:
                    list_product_ids.append(item.product_id)
                total = answer.result.total
                last_id = answer.result.last_id
    return list_product_ids


async def get_card_products(client_id: str, api_key: str) -> list[DataOzProductCard]:
    list_card_product = []
    list_product_ids = await get_products_ids(client_id=client_id, api_key=api_key)
    api_user = OzonApi(client_id=client_id, api_key=api_key)
    for ids in [list_product_ids[i:i + 100] for i in range(0, len(list_product_ids), 100)]:
        answer = await api_user.get_product_info_list(product_id=ids)
        attributes = await api_user.get_products_info_attributes(product_id=[str(product) for product in ids],
                                                                 limit=1000)
        if answer:
            if answer.result:
                for item in answer.result.items:
                    vendor_code = item.offer_id
                    brand = None
                    category = None
                    if attributes:
                        if attributes.result:
                            for product in attributes.result:
                                if product.id_field == item.id_field:
                                    for attribute in product.attributes:
                                        if attribute.attribute_id == 8229:
                                            category = attribute.values[0].value
                                        elif attribute.attribute_id == 85:
                                            brand = attribute.values[0].value
                    price = round(float(item.old_price), 2)
                    discount_price = round(float(item.price), 2)
                    for sku in [item.sku, item.fbo_sku, item.fbs_sku]:
                        if sku:
                            link = f"https://www.ozon.ru/product/{sku}"
                            list_card_product.append(DataOzProductCard(sku=str(sku),
                                                                       client_id=client_id,
                                                                       vendor_code=vendor_code,
                                                                       brand=brand,
                                                                       category=category,
                                                                       link=link,
                                                                       price=price,
                                                                       discount_price=discount_price))
    logger.info(f"Количество записей: {len(list_card_product)}")

    return list_card_product


async def get_adverts_campaigns(client_id: str, client_secret: str):
    api_user = OzonPerformanceAPI(client_id=client_id, client_secret=client_secret)
    answer = await api_user.get_client_statistics_daily_json()
    if answer:
        for advert in answer.rows:
            print(advert)


async def main_oz_advert(retries: int = 6) -> None:
    try:
        client_id = '25105183-1710665362610@advertising.performance.ozon.ru'
        client_secret = '5Hg7vS6gdJPMXgV7QnoM3oI-LcoNquKB1YhLoSalmY8W8z1nlHodpxlP9f4w3JRloDHgyVoUp0bdH0b5lw'
        db_conn = AzureDbConnection()
        db_conn.start_db()
        clients = db_conn.get_client(marketplace="Ozon")
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        date_yesterday = date - timedelta(days=1)

        for client in clients:
            await get_card_products(client.client_id, client.api_key)
            logger.info(f"Сбор карточек товаров {client.name_company}")

            logger.info(f"Сбор рекламных компаний {client.name_company}")

            logger.info(f"Статистика карточек товара {client.name_company} за {date_yesterday.date().isoformat()}")

            logger.info(f"Статистика рекламы {client.name_company} за {date_yesterday.date().isoformat()}")

    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_oz_advert(retries=retries - 1)
    #except Exception as e:
        #logger.error(f'{e}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_oz_advert())
    loop.stop()
