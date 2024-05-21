from typing import Optional

from .base import BaseResponse
from ..entities import ProductInfoList


class ProductInfoListResponse(BaseResponse):
    """Получить список товаров по идентификаторам."""
    result: Optional[ProductInfoList] = None
