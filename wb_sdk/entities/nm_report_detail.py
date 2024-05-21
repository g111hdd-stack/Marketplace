from typing import Optional
from pydantic import Field

from .base import BaseEntity


class NMReportDetailCardTag(BaseEntity):
    """Теги."""
    id_field: int = Field(default=None, alias='id')
    name: str = None


class NMReportDetailCardObject(BaseEntity):
    """Предмет."""
    id_field: int = Field(default=None, alias='id')
    name: str = None


class NMReportDetailCardStatisticsPeriodConversions(BaseEntity):
    """Конверсии."""
    addToCartPercent: int = None
    cartToOrderPercent: int = None
    buyoutsPercent: int = None


class NMReportDetailCardStatisticsPeriod(BaseEntity):
    """Статистика за период"""
    begin: str = None
    end: str = None
    openCardCount: float = None
    addToCartCount: float = None
    ordersCount: float = None
    ordersSumRub: float = None
    buyoutsCount: float = None
    buyoutsSumRub: float = None
    cancelCount: float = None
    cancelSumRub: float = None
    avgPriceRub: float = None
    avgOrdersCountPerDay: float = None
    conversions: Optional[NMReportDetailCardStatisticsPeriodConversions] = None


class NMReportDetailCardStatisticsPeriodComparison(BaseEntity):
    """Сравнение двух периодов, в процентах."""
    openCardDynamics: int = None
    addToCartDynamics: int = None
    ordersCountDynamics: int = None
    ordersSumRubDynamics: int = None
    buyoutsCountDynamics: int = None
    buyoutsSumRubDynamics: int = None
    cancelCountDynamics: int = None
    cancelSumRubDynamics: int = None
    avgOrdersCountPerDayDynamics: int = None
    avgPriceRubDynamics: int = None
    conversions: Optional[NMReportDetailCardStatisticsPeriodConversions] = None


class NMReportDetailCardStatistics(BaseEntity):
    """Статистика."""
    selectedPeriod: Optional[NMReportDetailCardStatisticsPeriod] = None
    previousPeriod: Optional[NMReportDetailCardStatisticsPeriod] = None
    periodComparison: Optional[NMReportDetailCardStatisticsPeriodComparison] = None


class NMReportDetailCardStocks(BaseEntity):
    """Остатки."""
    stocksMp: int = None
    stocksWb: int = None


class NMReportDetailCard(BaseEntity):
    """Статистики КТ."""
    nmID: int = None
    vendorCode: str = None
    brandName: str = None
    tags: Optional[list[NMReportDetailCardTag]] = []
    object: Optional[NMReportDetailCardObject] = None
    statistics: Optional[NMReportDetailCardStatistics] = None
    stocks: Optional[NMReportDetailCardStocks] = None


class NMReportDetailData(BaseEntity):
    """Статистики КТ."""
    page: int = None
    isNextPage: bool = None
    cards: Optional[list[NMReportDetailCard]] = []


class AdditionalErrors(BaseEntity):
    """Дополнительные ошибки."""
    field: str = None
    description: str = None
