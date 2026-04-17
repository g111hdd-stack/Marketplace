from typing import Optional

from .base import BaseRequest


class PromotionAdvertsRequest(BaseRequest):
    ids: Optional[str] = None
    status: int
    type: str
