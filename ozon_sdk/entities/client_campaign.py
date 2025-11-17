from datetime import datetime
from typing import Optional
from pydantic import Field

from .base import BaseEntity


class ExtCampaignCampaignAutopilotProperties(BaseEntity):
    """Информация о авто кампании."""
    categoryId: str = None
    skuAddMode: str = None


class ClientCampaign(BaseEntity):
    """Информация по РК."""
    id_field: str = Field(default=None, alias='id')
    paymentType: str = None
    title: str = None
    state: str = None
    advObjectType: str = None
    fromDate: str = None
    toDate: str = None
    isAutocreated: bool = None
    budget: str = None
    dailyBudget: str = None
    weeklyBudget: str = None
    placement: Optional[list[str]] = []
    productAutopilotStrategy: str = None
    autopilot: Optional[ExtCampaignCampaignAutopilotProperties] = None
    createdAt: datetime = None
    updatedAt: datetime = None
    productCampaignMode: str = None
