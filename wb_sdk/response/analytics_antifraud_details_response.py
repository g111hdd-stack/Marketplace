from typing import Optional

from .base import BaseResponse
from ..entities import AnalyticsAntifraudDetails


class AnalyticsAntifraudDetailsResponse(BaseResponse):
    """Возвращает отчёт по удержаниям за самовыкупы."""
    details: Optional[list[AnalyticsAntifraudDetails]] = []
