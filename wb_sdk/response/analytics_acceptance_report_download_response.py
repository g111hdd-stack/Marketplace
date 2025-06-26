from typing import Optional

from .base import BaseResponse
from ..entities import AnalyticsAcceptanceReportDownload


class AnalyticsAcceptanceReportDownloadResponse(BaseResponse):
    """Возвращает отчёт по приёмке."""
    result: Optional[list[AnalyticsAcceptanceReportDownload]] = []

