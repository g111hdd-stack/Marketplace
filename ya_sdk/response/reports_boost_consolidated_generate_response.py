from typing import Optional

from .base import BaseResponse
from ..entities import GenerateReportDTO


class ReportsBoostConsolidatedGenerateResponse(BaseResponse):
    """Отчет по бусту продаж."""
    status: str = None
    result: Optional[GenerateReportDTO] = None
