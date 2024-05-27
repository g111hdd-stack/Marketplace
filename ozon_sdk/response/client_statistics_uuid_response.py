from datetime import datetime
from typing import Optional

from .base import BaseResponse
from ..entities import ClientStatisticsUUID


class ClientStatisticsUUIDResponse(BaseResponse):
    """Cтатус отчёта."""
    UUID: str = None
    state: str = None
    createdAt: datetime = None
    updatedAt: datetime = None
    request: Optional[ClientStatisticsUUID] = None
    error: str = None
    link: str = None
    kind: str = None
