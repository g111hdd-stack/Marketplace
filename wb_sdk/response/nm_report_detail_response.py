from typing import Optional

from .base import BaseResponse
from ..entities import NMReportDetailData, AdditionalErrors


class NMReportDetailResponse(BaseResponse):
    """Статистика КТ за выбранный период."""
    data: Optional[NMReportDetailData] = None
    error: bool = None
    errorText: str = None
    additionalErrors: Optional[list[AdditionalErrors]] = []
