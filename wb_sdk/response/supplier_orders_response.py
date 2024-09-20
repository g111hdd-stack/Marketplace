from typing import Optional

from .base import BaseResponse
from ..entities import SupplierOrders


class SupplierOrdersResponse(BaseResponse):
    """Заказы."""
    result: Optional[list[SupplierOrders]] = []
