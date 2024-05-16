from .base import BaseResponse
from ..entities import FlippingPagerDTO, OrderDTO


class CampaignsOrdersResponse(BaseResponse):
    """Информация о заказах."""
    pager: FlippingPagerDTO
    orders: list[OrderDTO] = []
