from typing import Optional

from .base import BaseRequest


class PromotionAdvertsRequest(BaseRequest):
    ids: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
