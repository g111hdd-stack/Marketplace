from typing import Optional

from .base import BaseResponse
from ..entities import ProductsInfoAttributes


class ProductsInfoAttributesResponse(BaseResponse):
    result: Optional[list[ProductsInfoAttributes]] = []
    last_id: str = None
    total: int = None
