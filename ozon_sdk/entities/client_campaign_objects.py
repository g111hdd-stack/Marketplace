from pydantic import Field

from .base import BaseEntity


class ClientCampaignObject(BaseEntity):
    """Информация по объектам РК."""
    id_field: str = Field(default=None, alias='id')
