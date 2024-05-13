from .base import BaseRequest


class PromotionAdvertsRequest(BaseRequest):
    status: int
    type: int
    order: str
    direction: str
