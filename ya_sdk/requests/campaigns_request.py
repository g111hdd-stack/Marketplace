from typing import Optional

from .base import BaseRequest


class CampaignsRequest(BaseRequest):
    """Магазины пользователя."""
    page: Optional[int] = 1
    pageSize: Optional[int] = None
