from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import BaseEntity


class ClientStatisticsUUID(BaseEntity):
    """Структура исходного запроса."""
    campaigns: Optional[list[str]] = []
    from_field: datetime = Field(None, alias='from')
    to: datetime = None
    dateFrom: str = None
    dateTo: str = None
    groupBy: str = None
