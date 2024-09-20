from typing import Optional

from .base import BaseResponse
from ..entities import Fullstats


class FullstatsResponse(BaseResponse):
    """Возвращает статистику кампаний."""
    result: Optional[list[Fullstats]] = []
