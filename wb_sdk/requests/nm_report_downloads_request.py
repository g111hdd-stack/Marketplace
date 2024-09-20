from typing import Optional
from pydantic import Field

from .base import BaseRequest


class NmReportDownloadsParamsRequest(BaseRequest):
    """Параметры отчёта."""
    nmIDs: Optional[list[int]] = []
    subjectIDs: Optional[list[int]] = []
    brandNames: Optional[list[str]] = []
    tagIDs: Optional[list[int]] = []
    startDate: str
    endDate: str
    timezone: str = 'Europe/Moscow'
    aggregationLevel: str = 'day'
    skipDeletedNm: bool = False


class NmReportDownloadsRequest(BaseRequest):
    """Создать отчёт по воронке продаж."""
    id_field: str = Field(alias='id')
    reportType: Optional[str] = 'DETAIL_HISTORY_REPORT'
    userReportName: Optional[str] = ''
    params: NmReportDownloadsParamsRequest
