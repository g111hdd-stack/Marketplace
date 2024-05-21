from typing import Optional
from pydantic import Field

from .base import BaseRequest


class ClientStatisticsJSONRequest(BaseRequest):
    campaigns: Optional[list[str]] = None
    from_field: Optional[str] = Field(default=None, serialization_alias='from')
    to: Optional[str] = None
    dateFrom: Optional[str] = None
    dateTo: Optional[str] = None
    groupBy: Optional[str] = None
