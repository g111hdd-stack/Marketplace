from datetime import date

from .base import BaseEntity


class AnalyticsAcceptanceReportDownload(BaseEntity):
    """Отчёт о приёмке."""
    count: int = None
    giCreateDate: date = None
    incomeId: int = None
    nmID: int = None
    shkCreateDate: date = None
    subjectName: str = None
    total: float = None
