from typing import Optional

from .base import BaseResponse
from ..entities import OrderServiceOrderGet


class OrderServiceOrderGetResponse(BaseResponse):
    data: OrderServiceOrderGet
    meta: Optional[dict] = {}
