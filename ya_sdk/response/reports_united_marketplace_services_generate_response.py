from typing import Optional

from .base import BaseResponse
from ..entities import GenerateReportDTO


class ReportsUnitedMarketplaceServicesGenerateResponse(BaseResponse):
    """Отчет по стоимости услуг."""
    status: str = None
    result: Optional[GenerateReportDTO] = None
