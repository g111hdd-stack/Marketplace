from typing import Optional

from .base import BaseResponse
from ..entities import ClientStatisticsDailyJSON


class ClientStatisticsDailyJSONResponse(BaseResponse):
    rows: Optional[list[ClientStatisticsDailyJSON]] = []
