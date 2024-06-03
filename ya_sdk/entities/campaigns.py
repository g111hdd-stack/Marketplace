from typing import Optional
from pydantic import Field

from .base import BaseEntity


class BusinessDTO(BaseEntity):
    field_id: int = Field(None, alias='id')
    name: str = None


class CampaignDTO(BaseEntity):
    domain: str = None
    field_id: int = Field(None, alias='id')
    clientId: int = None
    business: Optional[BusinessDTO] = None
    placementType: str = None
