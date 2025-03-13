from typing import Optional

from .base import BaseResponse
from ..entities import FlippingPagerDTO, OrderDTO


class CampaignsOrdersResponse(BaseResponse):
    """Информация о заказах."""
    pager: Optional[FlippingPagerDTO] = None
    orders: list[OrderDTO] = []
