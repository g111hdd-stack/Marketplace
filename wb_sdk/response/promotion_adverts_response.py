from typing import Optional

from .base import BaseResponse
from ..entities import PromotionAdverts


class PromotionAdvertsResponse(BaseResponse):
    """Информация о кампаниях."""
    result: Optional[list[PromotionAdverts]] = []
