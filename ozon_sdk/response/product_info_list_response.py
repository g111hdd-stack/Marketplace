from typing import Optional

from .base import BaseResponse
from ..entities import ProductInfoListItem


class ProductInfoListResponse(BaseResponse):
    """Получить список товаров по идентификаторам."""
    items: Optional[list[ProductInfoListItem]] = []
