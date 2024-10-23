from typing import Optional

from .base import BaseResponse
from ..entities import ProductInfoDiscounted


class ProductInfoDiscountedResponse(BaseResponse):
    """Получить информацию о состоянии и дефектах уценённого товара по его SKU."""
    items: Optional[list[ProductInfoDiscounted]] = []
