from typing import Optional

from .base import BaseRequest


class SupplierReportDetailByPeriodRequest(BaseRequest):
    dateFrom: str
    limit: Optional[int] = 100000
    dateTo: str
    rrdid: Optional[int] = 0
