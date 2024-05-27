from typing import Optional

from .base import BaseRequest


class AnalyticsDataFilter(BaseRequest):
    """Фильтры."""
    key: Optional[str] = None
    op: Optional[str] = None
    value: Optional[str] = None


class AnalyticsDataSort(BaseRequest):
    """Настройки сортировки отчёта."""
    key: Optional[str] = None
    order: Optional[str] = None


class AnalyticsDataRequest(BaseRequest):
    """Данные аналитики."""
    date_from: str
    date_to: str
    dimension: list[str]
    filters: Optional[list[AnalyticsDataFilter]] = []
    limit: Optional[int] = 100
    metrics: list[str]
    offset: Optional[int] = 0
    sort: Optional[list[AnalyticsDataSort]] = []
