from pydantic import Field
from typing import Optional

from .base import BaseEntity


class PromotionAdvertsNMSettingsBids(BaseEntity):
    """Ставки, копейки."""
    search: Optional[int] = None
    recommendations: Optional[int] = None

class PromotionAdvertsNMSettingsSubject(BaseEntity):
    """Предмет."""
    field_id: int = Field(alias='id')
    name: Optional[str] = None

class PromotionAdvertsNMSettings(BaseEntity):
    """Настройки товара."""
    bids_kopecks: Optional[PromotionAdvertsNMSettingsBids] = None
    subject: Optional[PromotionAdvertsNMSettingsSubject] = None
    nm_id: Optional[int] = None

class PromotionAdvertsSettingsPlacements(BaseEntity):
    """Места размещения."""
    search: Optional[bool] = None
    recommendations: Optional[bool] = None

class PromotionAdvertsSettings(BaseEntity):
    """Настройки кампании."""
    payment_type: Optional[str] = None
    name: Optional[str] = None
    placements: Optional[PromotionAdvertsSettingsPlacements]

class PromotionAdvertsPromotionAdverts(BaseEntity):
    """Временные отметки."""
    created: Optional[str] = None
    updated: Optional[str] = None
    started: Optional[str] = None
    deleted: Optional[str] = None

class PromotionAdverts(BaseEntity):
    """Информация о кампаниях."""
    bid_type: str = None
    advertId: int = Field(alias='id')
    nm_settings: Optional[list[PromotionAdvertsNMSettings]] = []
    settings: Optional[PromotionAdvertsSettings] = None
    status: int = None
    timestamps: Optional[PromotionAdvertsPromotionAdverts] = None
