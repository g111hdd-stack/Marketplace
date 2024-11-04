from typing import Optional

from .base import BaseRequest


class CampaignsOffersStocksQueryRequest(BaseRequest):
    """Детальная информация по остаткам на складах. Query."""
    page_token: Optional[str]
    limit: int = 20


class CampaignsOffersStocksBodyRequest(BaseRequest):
    """Детальная информация по остаткам на складах. Body."""
    archived: Optional[bool]
    offerIds: Optional[list[str]] = []
    withTurnover: Optional[bool] = False
