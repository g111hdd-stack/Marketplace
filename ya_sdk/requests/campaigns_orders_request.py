from enum import Enum
from typing import Optional

from .base import BaseRequest


class OrderStatusType(str, Enum):
    """
        CANCELLED — заказ отменен. \n
        DELIVERED — заказ получен покупателем. \n
        DELIVERY — заказ передан в службу доставки. \n
        PICKUP — заказ доставлен в пункт самовывоза. \n
        PROCESSING — заказ находится в обработке. \n
        PENDING — заказ ожидает обработки продавцом. \n
        UNPAID — заказ оформлен, но еще не оплачен (если выбрана оплата при оформлении). \n
        PLACING — заказ оформляется, подготовка к резервированию. \n
        RESERVED — заказ pарезервирован, но недооформлен. \n
        PARTIALLY_RETURNED — частичный возврат. \n
        RETURNED — полный возврат. \n
        UNKNOWN — неизвестный статус.
    """
    EMPTY = ''
    CANCELLED = 'CANCELLED'
    DELIVERED = 'DELIVERED'
    DELIVERY = 'DELIVERY'
    PICKUP = 'PICKUP'
    PROCESSING = 'PROCESSING'
    PENDING = 'PENDING'
    UNPAID = 'UNPAID'
    PLACING = 'PLACING'
    RESERVED = 'RESERVED'
    PARTIALLY_RETURNED = 'PARTIALLY_RETURNED'
    RETURNED = 'RETURNED'
    UNKNOWN = 'UNKNOWN'


class OrderSubstatusType(str, Enum):
    """
        STARTED — заказ подтвержден, его можно начать обрабатывать. \n
        READY_TO_SHIP — заказ собран и готов к отправке. \n
        PROCESSING_EXPIRED — значение более не используется. \n
        REPLACING_ORDER — покупатель решил заменить товар другим по собственной инициативе. \n
        RESERVATION_EXPIRED — покупатель не завершил оформление зарезервированного заказа в течение 10 минут. \n
        SHOP_FAILED — магазин не может выполнить заказ. \n
        USER_CHANGED_MIND — покупатель отменил заказ по личным причинам. \n
        USER_NOT_PAID — покупатель не оплатил заказ в течение 30 минут. \n
        USER_REFUSED_DELIVERY — покупателя не устроили условия доставки. \n
        USER_REFUSED_PRODUCT — покупателю не подошел товар. \n
        USER_REFUSED_QUALITY — покупателя не устроило качество товара. \n
        USER_UNREACHABLE — не удалось связаться с покупателем.
    """
    EMPTY = ''
    STARTED = 'STARTED'
    READY_TO_SHIP = 'READY_TO_SHIP'
    PROCESSING_EXPIRED = 'PROCESSING_EXPIRED'
    REPLACING_ORDER = 'REPLACING_ORDER'
    RESERVATION_EXPIRED = 'RESERVATION_EXPIRED'
    SHOP_FAILED = 'SHOP_FAILED'
    USER_CHANGED_MIND = 'USER_CHANGED_MIND'
    USER_NOT_PAID = 'USER_NOT_PAID'
    USER_REFUSED_DELIVERY = 'USER_REFUSED_DELIVERY'
    USER_REFUSED_PRODUCT = 'USER_REFUSED_PRODUCT'
    USER_REFUSED_QUALITY = 'USER_REFUSED_QUALITY'
    USER_UNREACHABLE = 'USER_UNREACHABLE'


class OrderDeliveryDispatchType(str, Enum):
    """
        BUYER — доставка покупателю. \n
        MARKET_PARTNER_OUTLET — доставка в пункт выдачи партнера. \n
        MARKET_BRANDED_OUTLET — доставка в пункт выдачи заказов Маркета. \n
        SHOP_OUTLET — доставка в пункт выдачи заказов магазина. \n
        DROPOFF — доставка в пункт выдачи, который принимает заказы от продавцов и передает их курьерам. \n
        UNKNOWN — неизвестный тип.
    """
    EMPTY = ''
    BUYER = 'BUYER'
    MARKET_PARTNER_OUTLET = 'MARKET_PARTNER_OUTLET'
    MARKET_BRANDED_OUTLET = 'MARKET_BRANDED_OUTLET'
    SHOP_OUTLET = 'SHOP_OUTLET'
    DROPOFF = 'DROPOFF'
    UNKNOWN = 'UNKNOWN'


class OrderBuyerType(str, Enum):
    """
        PERSON — физическое лицо. \n
        BUSINESS — организация.
    """
    EMPTY = ''
    PERSON = 'PERSON'
    BUSINESS = 'BUSINESS'


class CampaignsOrdersRequest(BaseRequest):
    """Информация о заказах."""
    orderIds: Optional[list[int]]
    status: Optional[list[str]]
    substatus: Optional[list[str]]
    fromDate: Optional[str]
    toDate: Optional[str]
    supplierShipmentDateFrom: Optional[str]
    supplierShipmentDateTo: Optional[str]
    updatedAtFrom: Optional[str]
    updatedAtTo: Optional[str]
    dispatchType: Optional[str]
    fake: bool = False
    hasCis: bool = False
    onlyWaitingForCancellationApprove: bool = False
    onlyEstimatedDelivery: bool = False
    buyerType: Optional[str]
    page: int = 1
    pageSize: int = 50


