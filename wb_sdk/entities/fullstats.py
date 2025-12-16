from datetime import date, datetime
from pydantic import Field
from typing import Optional

from .base import BaseEntity


class FullstatsDaysAppNM(BaseEntity):
    """Блок статистики по артикулам WB."""
    views: int = None
    clicks: int = None
    ctr: float = None
    cpc: float = None
    sum: float = None
    atbs: int = None
    orders: int = None
    cr: float = None
    shks: int = None
    sum_price: float = None
    name: str = None
    nmId: int = None


class FullstatsDaysApp(BaseEntity):
    """Блок информации о платформе."""
    views: int = None
    clicks: int = None
    ctr: float = None
    cpc: float = None
    sum: float = None
    atbs: int = None
    orders: int = None
    cr: float = None
    shks: int = None
    sum_price: float = None
    nms: Optional[list[FullstatsDaysAppNM]] = []
    appType: int = None


class FullstatsDay(BaseEntity):
    """Статистка по дням."""
    date_field: datetime = Field(default=None, alias='date')
    views: int = None
    canceled: int = None
    clicks: int = None
    ctr: float = None
    cpc: float = None
    sum: float = None
    atbs: int = None
    orders: int = None
    cr: float = None
    shks: int = None
    sum_price: float = None
    apps: Optional[list[FullstatsDaysApp]] = []


class FullstatsDayBoosterStats(BaseEntity):
    """Статистика по средней позиции товара на страницах поисковой выдачи и каталога (для автоматических кампаний)."""
    date_field: str = Field(default=None, alias='date')
    nm: int = None
    avg_position: int = None


class Fullstats(BaseEntity):
    """Статистика кампании."""
    views: int = None
    canceled: int = None
    clicks: int = None
    ctr: float = None
    cpc: float = None
    sum: float = None
    atbs: int = None
    orders: int = None
    cr: float = None
    shks: int = None
    sum_price: float = None
    days: Optional[list[FullstatsDay]] = []
    boosterStats: Optional[list[FullstatsDayBoosterStats]] = []
    advertId: int = None
