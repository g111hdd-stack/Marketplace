from typing import Optional

from .base import BaseResponse
from ..entities import ProductList


class ProductListResponse(BaseResponse):
    """Список товаров."""
    result: Optional[ProductList] = None
