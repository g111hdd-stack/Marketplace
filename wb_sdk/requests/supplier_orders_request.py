from .base import BaseRequest


class SupplierOrdersRequest(BaseRequest):
    """Запрос отчета о заказах."""
    dateFrom: str
    flag: int = 0
