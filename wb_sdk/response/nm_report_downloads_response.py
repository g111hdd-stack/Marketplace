from typing import Optional

from .base import BaseResponse
from ..entities import Error


class NmReportDownloadsResponse(BaseResponse):
    """Создать отчёт по воронке продаж."""
    data: str
    error: Optional[bool] = None
    errorText: Optional[str] = None
    additionalErrors: Optional[list[Error]] = []
