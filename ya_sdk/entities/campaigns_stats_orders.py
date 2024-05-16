from typing import Optional
from pydantic import Field

from .base import BaseEntity


class OrdersStatsDeliveryRegionDTO(BaseEntity):
    """Информация о регионе доставки."""
    id_field: int = Field(default=None, alias='id')
    name: str = None


class OrdersStatsPriceDTO(BaseEntity):
    """Цена или скидки на товар."""
    type: str = None
    costPerItem: float = None
    total: float = None


class OrdersStatsWarehouseDTO(BaseEntity):
    """Информация о складе, на котором хранится товар."""
    id_field: int = Field(default=None, alias='id')
    name: str = None


class OrdersStatsDetailsDTO(BaseEntity):
    """Информация об удалении товара из заказа."""
    itemStatus: str = None
    itemCount: int = None
    updateDate: str = None
    stockType: str = None


class OrdersStatsItemDTO(BaseEntity):
    """Список товаров в заказе после возможных изменений."""
    offerName: str = None
    marketSku: int = None
    shopSku: str = None
    count: int = None
    prices: Optional[list[OrdersStatsPriceDTO]] = []
    warehouse: Optional[OrdersStatsWarehouseDTO] = None
    details: Optional[list[OrdersStatsDetailsDTO]] = []
    cisList: Optional[list[str]] = []
    initialCount: int = None
    bidFee: int = None
    cofinanceThreshold: float = None
    cofinanceValue: float = None


class OrdersStatsPaymentOrderDTO(BaseEntity):
    """Информация о платежном получении."""
    id_field: int = Field(default=None, alias='id')
    date: str = None


class OrdersStatsPaymentDTO(BaseEntity):
    """Информация о денежных переводах по заказу."""
    id_field: int = Field(default=None, alias='id')
    date: str = None
    type: str = None
    source: str = None
    total: float = None
    paymentOrder: Optional[OrdersStatsPaymentOrderDTO] = None


class OrdersStatsCommissionDTO(BaseEntity):
    """Информация о стоимости услуг."""
    type: str = None
    actual: float = None


class OrdersStatsOrderDTO(BaseEntity):
    """Информация о заказе."""
    id_field: int = Field(default=None, alias='id')
    creationDate: str = None
    statusUpdateDate: str = None
    status: str = None
    partnerOrderId: str = None
    paymentType: str = None
    fake: bool = None
    deliveryRegion: Optional[OrdersStatsDeliveryRegionDTO] = None
    items: Optional[list[OrdersStatsItemDTO]] = []
    initialItems: Optional[list[OrdersStatsItemDTO]] = []
    payments: Optional[list[OrdersStatsPaymentDTO]] = []
    commissions: Optional[list[OrdersStatsCommissionDTO]] = []


class ForwardScrollingPagerDTO(BaseEntity):
    """Ссылка на следующую страницу."""
    nextPageToken: str = None


class OrdersStatsDTO(BaseEntity):
    """Информация по заказам."""
    orders: Optional[list[OrdersStatsOrderDTO]] = []
    paging: Optional[ForwardScrollingPagerDTO] = None
