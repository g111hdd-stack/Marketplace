from typing import Optional

from .base import BaseResponse
from ..entities import OrderServiceOrderSearch


class OrderServiceOrderSearchResponse(BaseResponse):
    success: int
    data: OrderServiceOrderSearch
    meta: Optional[dict] = {}
