from typing import Optional

from .base import BaseRequest


class CampaignsStatsOrdersQueryRequest(BaseRequest):
    """Детальная информация по заказам. Query."""
    page_token: Optional[str]
    limit: int = 20


class CampaignsStatsOrdersBodyRequest(BaseRequest):
    """Детальная информация по заказам. Body."""
    dateFrom: Optional[str]
    dateTo: Optional[str]
    updateFrom: Optional[str]
    updateTo: Optional[str]
    orders: Optional[list[int]]
    statuses: Optional[list[str]]
    hasCis: bool = False
