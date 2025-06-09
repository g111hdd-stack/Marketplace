import json
import asyncio
import logging
import nest_asyncio

from typing import List
from aiohttp import ClientSession, TCPConnector

from database.async_db import AsyncDbConnection
from data_classes import DataQuery, DataRating

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

URL = "https://search.wb.ru/exactmatch/ru/female/v9/search"
MAX_PAGE = 1
NUM_WORKERS = 4

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


async def pars_query(session: ClientSession, query: DataQuery, db_conn: AsyncDbConnection) -> None:
    query_text = query.query.strip().lower()
    sku = query.sku
    product = f"{query.vendor_code}({sku}) ИП {query.entrepreneur}"
    logger.info(f"{product}: {query_text}")

    for page in range(1, MAX_PAGE + 1):
        params = {
            "ab_testing": "false",
            "appType": 64,
            "curr": "rub",
            "dest": 123585762,
            "hide_dtype": 13,
            "lang": "ru",
            "page": page,
            "query": query_text,
            "resultset": "catalog",
            "sort": "popular"
        }

        async with session.get(URL, params=params, headers=HEADERS) as response:
            if response.content_type != 'application/json':
                text = await response.text()
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    logger.error(f"{product}: {query_text} - Ошибка парсинга JSON")
                    return
            else:
                data = await response.json()

            cards = data.get("data", {}).get("products", [])

            if not cards:
                logger.error(f"{product}: {query_text} - Данные отсутствуют")

            target_card = next((card for card in cards if str(card.get("id")) == sku), None)
            if not target_card:
                continue

            stat = target_card.get("log")
            if not isinstance(stat, dict):
                logger.error(f"{product}: {query_text} - Карточка найдена, но нет данных по промо")
                continue

            cpm = stat.get("cpm")
            promo_position = stat.get("promoPosition")
            position = stat.get("position")
            advert_id = stat.get("advertId")

            if all([m is None for m in [cpm, promo_position, position, advert_id]]):
                logger.error(f"{product}: {query_text} - Карточка найдена, но нет данных по промо в log")
                continue

            await db_conn.add_rating(
                DataRating(query_id=query.id_query,
                           cpm=float(cpm) if cpm is not None else None,
                           promo_position=int(promo_position) if promo_position is not None else None,
                           position=int(position) if position is not None else None,
                           advert_id=str(advert_id) if advert_id is not None else None))
            info = f"Позиция в промо: {promo_position} | Позиция: {position} | CPM: {cpm} | РК: {advert_id}"
            logger.info(f"{product}: {query_text} - {info}")
            return
    else:
        logger.info(f"Товар не найден на первых {MAX_PAGE} страницах")
        await db_conn.add_rating(DataRating(query_id=query.id_query,
                                            cpm=None,
                                            promo_position=100,
                                            position=None,
                                            advert_id=None))


async def run_async_worker():
    db_conn = AsyncDbConnection()
    queries = await db_conn.get_queries()

    connector = TCPConnector(limit=4)
    async with ClientSession(connector=connector) as session:
        tasks = [pars_query(session, query, db_conn) for query in queries]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(run_async_worker())
