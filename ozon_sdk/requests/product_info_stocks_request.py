from typing import Optional

from .base import BaseRequest


class ProductInfoStocksFilter(BaseRequest):
    """Фильтр по товарам."""
    offer_id: Optional[list[str]] = []
    product_id: Optional[list[str]] = []
    visibility: Optional[str] = 'ALL'


class ProductInfoStocksRequest(BaseRequest):
    """Список товаров."""
    filter: Optional[ProductInfoStocksFilter]
    last_id: Optional[str]
    limit: Optional[int] = 100
