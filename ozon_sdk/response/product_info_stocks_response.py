from typing import Optional

from .base import BaseResponse
from ..entities import ProductInfoStocksItem


class ProductInfoStocksResponse(BaseResponse):
    """Получить остатки на складах."""
    cursor: str = None
    items: Optional[list[ProductInfoStocksItem]] = []
    total: int = None
