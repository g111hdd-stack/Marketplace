from typing import Optional

from .base import BaseRequest


class ProductInfoStocksFilterWithQuant(BaseRequest):
    created: Optional[bool] = None
    exists: Optional[bool] = None


class ProductInfoStocksFilter(BaseRequest):
    """Фильтр по товарам."""
    offer_id: Optional[list[str]] = []
    product_id: Optional[list[str]] = []
    visibility: Optional[str] = 'ALL'
    with_quant: Optional[ProductInfoStocksFilterWithQuant] = None


class ProductInfoStocksRequest(BaseRequest):
    """Список товаров."""
    cursor: Optional[str]
    filter: Optional[ProductInfoStocksFilter]
    limit: Optional[int] = 100
