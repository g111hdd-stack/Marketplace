from datetime import date
from pydantic import Field

from .base import BaseEntity


class AnalyticsAcceptanceReport(BaseEntity):
    """Отчёт о приёмке."""
    count: int = None
    giCreateDate: date = None
    incomeId: int = None
    nmID: int = None
    shkCreateDate: date = Field(default=None, alias='shkСreateDate')
    subjectName: str = None
    total: float = None
