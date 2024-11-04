from typing import Optional

from .base import BaseEntity


class WarehouseStockDTO(BaseEntity):
    """Информация об остатках товара."""
    count: int = None
    type: str = None


class TurnoverDTO(BaseEntity):
    """Информация об оборачиваемости товара."""
    turnover: str
    turnoverDays: float = None


class WarehouseOfferDTO(BaseEntity):
    """Информация об остатках товара."""
    offerId: str = None
    stocks: list[WarehouseStockDTO] = []
    turnoverSummary: Optional[TurnoverDTO] = None
    updatedAt: str = None


class WarehouseOffersDTO(BaseEntity):
    """Информация об остатках товаров на складе."""
    offers: list[WarehouseOfferDTO] = []
    warehouseId: int = None


class ScrollingPagerDTO(BaseEntity):
    """Информация о страницах результатов."""
    nextPageToken: str = None
    prevPageToken: str = None


class GetWarehouseStocksDTO(BaseEntity):
    """Список складов с информацией об остатках на каждом из них."""
    warehouses: list[WarehouseOffersDTO] = []
    paging: Optional[ScrollingPagerDTO] = []
