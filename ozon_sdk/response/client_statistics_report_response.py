from typing import Optional

from .base import BaseResponse
from ..entities import ClientStatisticsReport


class ClientStatisticsReportResponse(BaseResponse):
    """Получить отчёты."""
    result: Optional[list[ClientStatisticsReport]] = []
