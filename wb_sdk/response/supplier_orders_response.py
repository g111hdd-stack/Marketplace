from .base import BaseResponse
from ..entities import SupplierOrders


class SupplierOrdersResponse(BaseResponse):
    """Заказы."""
    result: list[SupplierOrders] = []
