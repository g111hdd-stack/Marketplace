from typing import Optional

from .base import BaseResponse
from ..entities import PromotionAdverts


class PromotionAdvertsResponse(BaseResponse):
    """Информация о кампаниях."""
    adverts: Optional[list[PromotionAdverts]] = []
