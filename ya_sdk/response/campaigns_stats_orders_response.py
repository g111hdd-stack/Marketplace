from typing import Optional

from .base import BaseResponse
from ..entities import OrdersStatsDTO


class CampaignsStatsOrdersResponse(BaseResponse):
    """Детальная информация по заказам."""
    status: str = None
    result: Optional[OrdersStatsDTO] = None
