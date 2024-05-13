from typing import Optional

from .base import BaseRequest


class ListGoodsFilterRequest(BaseRequest):
    """Возвращает информацию о товаре по его артикулу."""
    limit: int = 10
    offset: int = 0
    filterNmID: Optional[int]
