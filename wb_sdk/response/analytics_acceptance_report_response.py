from typing import Optional

from .base import BaseResponse
from ..entities import AnalyticsAcceptanceReport


class AnalyticsAcceptanceReportResponse(BaseResponse):
    """Возвращает отчёт по приёмке."""
    report: Optional[list[AnalyticsAcceptanceReport]] = []
