from datetime import datetime
from typing import Optional

from .base import BaseEntity


class OrderServiceOrderGetItemDiscount(BaseEntity):
    discountType: str = None
    discountDescription: str = None
    discountAmount: int = None


class OrderServiceOrderGetItemGoods(BaseEntity):
    name: str = None
    categoryName: str = None


class OrderServiceOrderGetItemBox(BaseEntity):
    boxIndex: str = None
    boxCode: str = None


class OrderServiceOrderGetItem(BaseEntity):
    itemIndex: str = None
    status: str = None
    price: int = None
    finalPrice: int = None
    discounts: Optional[list[OrderServiceOrderGetItemDiscount]] = []
    quantity: int = None
    offerId: str = None
    goodsId: str = None
    goodsData: OrderServiceOrderGetItemGoods
    boxes: Optional[list[OrderServiceOrderGetItemBox]] = []


class OrderServiceOrderGetShipment(BaseEntity):
    shipmentId: str = None
    orderCode: Optional[str] = None
    confirmedTimeLimit: str = None
    packingTimeLimit: str = None
    shipmentDateFrom: str = None
    shipmentDateTo: str = None
    packingDate: str = None
    reserveExpirationDate: Optional[str] = None
    deliveryId: str = None
    shipmentDateShift: bool = None
    shipmentIsChangeable: bool = None
    customerFullName: str = None
    customerAddress: str = None
    shippingPoint: str = None
    creationDate: str = None
    deliveryDate: str = None
    deliveryDateFrom: str = None
    deliveryDateTo: str = None
    items: Optional[list[OrderServiceOrderGetItem]] = []
    deliveryMethodId: str = None
    depositedAmount: int = None
    serviceScheme: str = None
    customer: Optional[str] = None
    status: str = None


class OrderServiceOrderGet(BaseEntity):
    shipments: Optional[list[OrderServiceOrderGetShipment]] = []


