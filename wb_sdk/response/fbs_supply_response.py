import datetime

from pydantic import Field
from typing import Optional

from .base import BaseResponse


class FBSSupplyResponse(BaseResponse):
    """Возвращает информацию о поставке FBS."""
    id_field: str = Field(default=None, alias='id')
    done: bool = None
    createdAt: Optional[datetime.datetime] = None
    closedAt:  Optional[datetime.datetime] = None
    scanDt:  Optional[datetime.datetime] = None
    name: str = None
    cargoType: int = None
