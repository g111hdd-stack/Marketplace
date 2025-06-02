from typing import Optional

from .base import BaseResponse
from ..entities import GenerateReportDTO


class ReportsShowsBoostGenerateResponse(BaseResponse):
    """Отчет по бусту показов."""
    status: str = None
    result: Optional[GenerateReportDTO] = None
