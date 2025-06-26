from typing import Optional

from .base import BaseResponse
from ..entities import FBSWarehouses


class FBSWarehousesResponse(BaseResponse):
    """Возвращает список складов FBS."""
    result: Optional[list[FBSWarehouses]] = []
