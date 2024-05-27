from typing import Optional

from .base import BaseResponse
from ..entities import AnalyticsData


class AnalyticsDataResponse(BaseResponse):
    """Данные аналитики."""
    result: Optional[AnalyticsData] = None
    timestamp: str = None
