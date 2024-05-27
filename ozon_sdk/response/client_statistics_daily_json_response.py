from typing import Optional

from .base import BaseResponse
from ..entities import ClientStatisticsDailyJSON


class ClientStatisticsDailyJSONResponse(BaseResponse):
    """Дневная статистика по кампаниям."""
    rows: Optional[list[ClientStatisticsDailyJSON]] = []
