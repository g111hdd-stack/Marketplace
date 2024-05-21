from typing import Optional

from .base import BaseRequest


class ProductListFilter(BaseRequest):
    """Фильтр по товарам."""
    offer_id: Optional[list[str]] = []
    product_id: Optional[list[str]] = []
    visibility: Optional[str] = 'ALL'


class ProductListRequest(BaseRequest):
    """Список товаров."""
    filter: Optional[ProductListFilter]
    last_id: Optional[str]
    limit: Optional[int] = 100
