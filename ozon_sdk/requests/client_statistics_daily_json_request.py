from typing import Optional

from .base import BaseRequest


class ClientStatisticsDailyJSONRequest(BaseRequest):
    campaignIds: Optional[list[str]] = []
    dateFrom: Optional[str] = None
    dateTo: Optional[str] = None
