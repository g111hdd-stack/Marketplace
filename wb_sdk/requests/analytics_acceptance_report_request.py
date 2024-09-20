from .base import BaseRequest


class AnalyticsAcceptanceReportRequest(BaseRequest):
    """Запрос отчёта по приёмке."""
    dateFrom: str
    dateTo: str
