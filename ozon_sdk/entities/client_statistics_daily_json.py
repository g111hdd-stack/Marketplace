from pydantic import Field

from .base import BaseEntity


class ClientStatisticsDailyJSON(BaseEntity):
    """Дневная статистика по кампаниям."""
    id_field: str = Field(default=None, alias='id')
    title: str = None
    date: str = None
    views: str = None
    clicks: str = None
    moneySpent: str = None
    avgBid: str = None
    orders: str = None
    ordersMoney: str = None
