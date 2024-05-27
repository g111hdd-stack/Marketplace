from typing import Optional
from pydantic import Field

from .base import BaseResponse
from ..entities import ClientCampaign


class ClientCampaignResponse(BaseResponse):
    """Список кампаний."""
    list_field: Optional[list[ClientCampaign]] = Field(default=[], alias='list')
