from typing import Optional

from .base import BaseRequest


class ProductInfoListRequest(BaseRequest):
    """Получить список товаров по идентификаторам."""
    offer_id: Optional[list[str]] = []
    product_id: Optional[list[str]] = []
    sku: Optional[list[int]] = []
