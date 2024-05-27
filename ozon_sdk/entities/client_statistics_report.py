from typing import Optional
from pydantic import Field

from .base import BaseEntity


class ClientStatisticReportRow(BaseEntity):
    """Данные по каждому sku."""
    date: str = None
    views: str = None
    clicks: str = None
    ctr: str = None
    moneySpent: str = None
    avgBid: str = None
    orders: str = None
    ordersMoney: str = None
    models: str = None
    modelsMoney: str = None
    sku: str = None
    title: str = None
    price: str = None


class ClientStatisticReportTotals(BaseEntity):
    """Общие данные."""
    views: str = None
    clicks: str = None
    ctr: str = None
    moneySpent: str = None
    avgBid: str = None
    orders: str = None
    ordersMoney: str = None
    models: str = None
    modelsMoney: str = None


class ClientStatisticReport(BaseEntity):
    """Данные отчёта."""
    rows: Optional[list[ClientStatisticReportRow]]
    totals: Optional[ClientStatisticReportTotals] = None


class ClientStatistic(BaseEntity):
    """Отчёт по рекламной компании."""
    title: str = None
    report: Optional[ClientStatisticReport] = None
    clicks: str = None
    ctr: str = None
    avgBid: str = None
    orders: str = None
    ordersMoney: str = None


class ClientStatisticsReport(BaseEntity):
    """Отчёт."""
    field_id: str = Field(None, alias='id')
    statistic: Optional[ClientStatistic] = None
