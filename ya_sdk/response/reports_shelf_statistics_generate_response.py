from typing import Optional

from .base import BaseResponse
from ..entities import GenerateReportDTO


class ReportsShelfStatisticsGenerateResponse(BaseResponse):
    """Отчет по полкам."""
    status: str = None
    result: Optional[GenerateReportDTO] = None
