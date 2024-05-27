from typing import Optional

from .base import BaseRequest


class ClientStatisticsDailyJSONRequest(BaseRequest):
    """Дневная статистика по кампаниям."""
    campaignIds: Optional[list[str]] = []
    dateFrom: Optional[str] = None
    dateTo: Optional[str] = None
