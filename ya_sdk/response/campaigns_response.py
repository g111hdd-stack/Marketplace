from typing import Optional

from .base import BaseResponse
from ..entities import FlippingPagerDTO, CampaignDTO


class CampaignsResponse(BaseResponse):
    """Магазины пользователя."""
    campaigns: Optional[list[CampaignDTO]] = []
    pager: Optional[FlippingPagerDTO] = None
