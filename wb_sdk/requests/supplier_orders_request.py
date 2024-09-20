from typing import Optional

from .base import BaseRequest


class SupplierOrdersRequest(BaseRequest):
    """Запрос отчета о заказах."""
    dateFrom: str
    flag: Optional[int] = 0
