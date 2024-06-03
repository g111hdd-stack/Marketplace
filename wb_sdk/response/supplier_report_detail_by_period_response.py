from typing import Optional

from .base import BaseResponse
from ..entities import SupplierReportDetailByPeriod


class SupplierReportDetailByPeriodResponse(BaseResponse):
    result: Optional[list[SupplierReportDetailByPeriod]] = []
