from .base import BaseRequest


class ClientStatisticsReportRequest(BaseRequest):
    """Получить отчёты."""
    UUID: str
