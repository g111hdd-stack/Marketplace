from typing import Optional
from pydantic import Field

from .base import BaseResponse
from ..entities import ClientCampaignObject


class ClientCampaignObjectsResponse(BaseResponse):
    """Список объектов компании «Вывод в топ», «Трафареты», «Баннеры» и «Видеобаннеры»"""
    list_field: Optional[list[ClientCampaignObject]] = Field(default=[], alias='list')
