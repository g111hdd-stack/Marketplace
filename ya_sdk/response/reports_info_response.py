from typing import Optional

from .base import BaseResponse
from ..entities import ReportInfoDTO


class ReportsInfoResponse(BaseResponse):
    """Статус генерации и скачивание готовых отчетов."""
    status: str = None
    result: Optional[ReportInfoDTO] = None
