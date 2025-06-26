from pydantic import Field

from .base import BaseResponse
from ..entities import FBSOrders


class FBSOrdersResponse(BaseResponse):
    """Возвращает информацию о сборочных заданиях FBS."""
    next_field: int = Field(default=None, alias='next')
    orders: list[FBSOrders] = []
