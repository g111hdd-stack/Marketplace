from typing import Optional

from .base import BaseRequest


class ClientCampaignRequest(BaseRequest):
    """Список кампаний."""
    campaignIds: Optional[list[str]] = []
    advObjectType: Optional[str] = None
    state: Optional[str] = None
    page: Optional[int] = None
    pageSize: Optional[int] = None
