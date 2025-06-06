import asyncio
import logging

from typing import List
from functools import wraps
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import ASYNC_DB_URL
from .models.async_models import *
from data_classes.general_dataclasses import DataRating, DataQuery

logger = logging.getLogger(__name__)


def async_retry_on_exception(retries=3, delay=10):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return await func(self, *args, **kwargs)
                except OperationalError as e:
                    attempt += 1
                    logger.debug(f"OperationalError: {e}. Retrying {attempt}/{retries} after {delay}s...")
                    await asyncio.sleep(delay)
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")
                    raise e
            raise RuntimeError("Max retries exceeded.")

        return wrapper

    return decorator


class AsyncDbConnection:
    def __init__(self, echo: bool = False) -> None:
        self.engine = create_async_engine(ASYNC_DB_URL, echo=echo, future=True)
        self.async_session = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)

    @async_retry_on_exception()
    async def start_db(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

    @async_retry_on_exception()
    async def add_rating(self, rating: DataRating) -> None:
        async with self.async_session() as session:
            new_rating = Rating(query_id=rating.query_id,
                                cpm=rating.cpm,
                                promo_position=rating.promo_position,
                                position=rating.position,
                                advert_id=rating.advert_id)
            session.add(new_rating)
            await session.commit()

    @async_retry_on_exception()
    async def get_queries(self) -> List[DataQuery]:
        async with self.async_session() as session:
            result = await session.execute(select(Query).options(selectinload(Query.product).selectinload(
                Product.client)).where(Query.is_track.is_(True)))
            queries = result.scalars().all()
            return [DataQuery(id_query=q.id_query,
                              query=q.query,
                              sku=q.product.sku,
                              vendor_code=q.product.vendor_code,
                              entrepreneur=q.product.client.entrepreneur) for q in queries]
