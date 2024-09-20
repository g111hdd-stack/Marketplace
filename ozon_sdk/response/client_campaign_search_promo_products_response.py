from typing import Optional
from pydantic import Field

from .base import BaseResponse
from ..entities import ClientCampaignObject


class ClientCampaignSearchPromoProductsResponse(BaseResponse):
    """Список объектов компании «Продвижение в поиске»."""
    list_field: Optional[list[ClientCampaignObject]] = Field(default=[], alias='list')
