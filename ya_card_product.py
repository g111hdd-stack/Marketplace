import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import OperationalError

from data_classes import DataYaOrder, DataYaCampaigns, DataYaCardProduct
from ya_sdk.ya_api import YandexApi
from database import YaDbConnection

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def add_yandex_card_product(db_conn: YaDbConnection, client_id: str, api_key: str) -> None:
    """
        Получает список товаров компании.

        Args:
            db_conn (YaDbConnection): Объект соединения с базой данных.
            client_id (str): ID кабинета.
            api_key (str): API KEY кабинета.
    """

    list_products = []

    # Инициализация API-клиента Yandex
    api_user = YandexApi(api_key=api_key)

    archived = [True, False]

    for archive in archived:
        page_token = None
        while True:
            answer = await api_user.get_businesses_offer_mappings(business_id=client_id,
                                                                  archived=archive,
                                                                  page_token=page_token)

            if not answer.result:
                break

            for product in answer.result.offerMappings:
                price = None
                discount_price = None
                vendor_code = product.offer.offerId

                if product.offer.basicPrice is not None:
                    price = product.offer.basicPrice.discountBase
                    discount_price = product.offer.basicPrice.value

                if product.mapping:
                    category = product.mapping.marketCategoryName
                    sku = str(product.mapping.marketSku)

                    list_products.append(DataYaCardProduct(sku=sku,
                                                           vendor_code=vendor_code,
                                                           client_id=client_id,
                                                           link=f"https://market.yandex.ru/search?text={sku}",
                                                           category=category,
                                                           archived=archive,
                                                           price=price or discount_price,
                                                           discount_price=discount_price))

            if not answer.result.paging.nextPageToken:
                break

            page_token = answer.result.paging.nextPageToken

    logger.info(f"Количество записей: {len(list_products)}")
    db_conn.add_ya_cards_products(list_card_product=list_products)


async def main(retries: int = 6) -> None:
    """
        Основная функция для обновления записей в базе данных.

        Получает список клиентов из базы данных,
        затем для каждого клиента добавляет записи за вчерашний день в таблицу `ya_main_table`.
    """
    try:
        db_conn = YaDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace='Yandex')
        for client in clients:
            logger.info(f"Добавление в базу данных компании '{client.name_company}'")
            await add_yandex_card_product(db_conn=db_conn,
                                          client_id=client.client_id,
                                          api_key=client.api_key)
    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.stop()
