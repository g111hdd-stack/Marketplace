from typing import Optional

from .base import BaseResponse
from ..entities import ListGoodsFilter


class ListGoodsFilterResponse(BaseResponse):
    """Информация о товаре."""
    data: Optional[ListGoodsFilter] = []

