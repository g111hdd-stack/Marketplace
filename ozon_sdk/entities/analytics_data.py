from typing import Optional
from pydantic import Field

from .base import BaseEntity


class AnalyticsDataDimensions(BaseEntity):
    """Группировка данных в отчёте."""
    id_field: str = Field(None, alias='id')
    name: str = None


class AnalyticsDataData(BaseEntity):
    """Массив данных."""
    dimensions: Optional[list[AnalyticsDataDimensions]] = []
    metrics: Optional[list[float]] = []


class AnalyticsData(BaseEntity):
    """Результаты запроса."""
    data: Optional[list[AnalyticsDataData]] = []
    totals: Optional[list[float]] = []
