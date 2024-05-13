from .base import BaseRequest


class SupplierSalesRequest(BaseRequest):
    """Запрос отчета о продажах по реализации."""
    dateFrom: str
    flag: int = 0
