from typing import Optional

from .base import BaseResponse
from ..entities import ProductInfoStocks


class ProductInfoStocksResponse(BaseResponse):
    """Получить остатки на складах."""
    result: Optional[ProductInfoStocks] = None
