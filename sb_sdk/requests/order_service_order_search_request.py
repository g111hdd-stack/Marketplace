from typing import Optional

from .base import BaseRequest


class OrderServiceOrderSearchDataRequest(BaseRequest):
    token: str
    dateFrom: str
    dateTo: str
    count: Optional[int] = 1000
    statuses: list[str]


class OrderServiceOrderSearchRequest(BaseRequest):
    data: OrderServiceOrderSearchDataRequest
    meta: Optional[dict] = {}
