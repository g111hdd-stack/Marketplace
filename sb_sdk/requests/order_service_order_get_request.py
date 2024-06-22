from typing import Optional

from .base import BaseRequest


class OrderServiceOrderGetDataRequest(BaseRequest):
    token: str
    shipments: list[str]
    merchantId: int


class OrderServiceOrderGetRequest(BaseRequest):
    data: OrderServiceOrderGetDataRequest
    meta: Optional[dict] = {}
