from .base import BaseRequest


class FinanceRealizationRequest(BaseRequest):
    """Отчёт о реализации товаров."""
    month: int
    year: int
