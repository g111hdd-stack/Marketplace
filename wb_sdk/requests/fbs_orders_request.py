from pydantic import Field
from typing import Optional

from .base import BaseRequest


class FBSOrdersRequest(BaseRequest):
    """Получить информацию о сборочных заданиях FBS."""
    limit: Optional[int] = 1000
    next_field: int = Field(default=0, alias='next')
    dateFrom: int
    dateTo: int
