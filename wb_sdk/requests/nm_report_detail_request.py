from typing import Optional

from .base import BaseRequest


class NMReportDetailPeriodRequest(BaseRequest):
    """Период."""
    begin: str
    end: str


class NMReportDetailOrderByRequest(BaseRequest):
    """Параметры сортировки."""
    field: str
    mode: str


class NMReportDetailRequest(BaseRequest):
    """Получение статистики КТ за выбранный период, по nmID/предметам/брендам/тегам."""
    brandNames: Optional[list[str]]
    objectIDs: Optional[list[int]]
    tagIDs: Optional[list[int]]
    nmIDs: Optional[list[int]]
    timezone: str
    period: Optional[NMReportDetailPeriodRequest]
    orderBy: Optional[NMReportDetailOrderByRequest]
    page: int

