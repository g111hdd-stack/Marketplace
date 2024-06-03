from typing import Optional
from pydantic import Field

from .base import BaseEntity


class OrderItemPromoDTO(BaseEntity):
    """Информация о вознаграждениях партнеру за скидки на товар по промокодам, купонам и акциям."""
    type_field: str = Field(default=None, alias='type')
    discount: float = None
    subsidy: float = None
    shopPromoId: str = None
    marketPromoId: str = None


class OrderItemInstanceDTO(BaseEntity):
    """Переданные вами для данной позиции коды маркировки или УИНы."""
    cis: str = None
    cisFull: str = None
    uin: str = None
    rnpt: str = None
    gtd: str = None


class OrderItemDetailDTO(BaseEntity):
    """Детали по товару в заказе."""
    itemCount: int = None
    itemStatus: str = None
    updateDate: str = None


class OrderItemSubsidyDTO(BaseEntity):
    """Общее вознаграждение партнеру за DBS-доставку и все скидки на товар."""
    type_field: str = Field(default=None, alias='type')
    amount: float = None


class OrderItemDTO(BaseEntity):
    """Список товаров в заказе."""
    id_field: int = Field(default=None, alias='id')
    offerId: str = None
    offerName: str = None
    price: float = None
    buyerPrice: float = None
    buyerPriceBeforeDiscount: float = None
    priceBeforeDiscount: float = None
    count: int = None
    vat: str = None
    shopSku: str = None
    subsidy: float = None
    partnerWarehouseId: str = None
    promos: list[OrderItemPromoDTO] = []
    instances: list[OrderItemInstanceDTO] = []
    details: list[OrderItemDetailDTO] = []
    subsidies: list[OrderItemSubsidyDTO] = []
    requiredInstanceTypes: list[str] = []


class OrderCourierDTO(BaseEntity):
    """Информация о курьере."""
    fullName: str = None
    phone: str = None
    phoneExtension: str = None
    vehicleNumber: str = None
    vehicleDescription: str = None


class OrderDeliveryDatesDTO(BaseEntity):
    """Диапазон дат доставки."""
    fromDate: str = None
    toDate: str = None
    fromTime: str = None
    toTime: str = None
    realDeliveryDate: str = None


class RegionDTO(BaseEntity):
    """Регион доставки."""
    id_field: int = Field(default=None, alias='id')
    name: str = None
    type_field: str = Field(default=None, alias='type')
    parent: Optional['RegionDTO'] = None
    children: list['RegionDTO'] = []


class GpsDTO(BaseEntity):
    """GPS-координаты широты и долготы."""
    latitude: float = None
    longitude: float = None


class OrderDeliveryAddressDTO(BaseEntity):
    """Адрес доставки."""
    country: str = None
    postcode: str = None
    city: str = None
    district: str = None
    subway: str = None
    street: str = None
    house: str = None
    block: str = None
    entrance: str = None
    entryphone: str = None
    floor: str = None
    apartment: str = None
    phone: str = None
    recipient: str = None
    gps: Optional[GpsDTO] = None


class OrderTrackDTO(BaseEntity):
    """Информация о трек-номере посылки (DBS)."""
    trackCode: str = None
    deliveryServiceId: int = None


class OrderParcelBoxDTO(BaseEntity):
    """Информация о грузоместе."""
    id_field: int = Field(default=None, alias='id')
    fulfilmentId: str = None


class OrderShipmentDTO(BaseEntity):
    """Список посылок."""
    id_field: int = Field(default=None, alias='id')
    status: str = None
    shipmentDate: str = None
    shipmentTime: str = None
    tracks: list[OrderTrackDTO] = []
    boxes: list[OrderParcelBoxDTO] = []


class OrderDeliveryDTO(BaseEntity):
    """Информация о доставке."""
    id_field: str = Field(default=None, alias='id')
    type_field: str = Field(default=None, alias='type')
    serviceName: str = None
    price: float = None
    deliveryPartnerType: str = None
    courier: Optional[OrderCourierDTO] = None
    dates: Optional[OrderDeliveryDatesDTO] = None
    region: Optional[RegionDTO] = None
    address: Optional[OrderDeliveryAddressDTO] = None
    vat: str = None
    deliveryServiceId: int = None
    liftType: str = None
    liftPrice: float = None
    outletCode: str = None
    outletStorageLimitDate: str = None
    dispatchType: str = None
    tracks: list[OrderTrackDTO] = []
    shipments: list[OrderShipmentDTO] = []
    estimated: bool = None
    eacType: str = None
    eacCode: str = None


class OrderBuyerDTO(BaseEntity):
    """Информация о покупателе."""
    id_field: str = Field(default=None, alias='id')
    lastName: str = None
    firstName: str = None
    middleName: str = None
    type_field: str = Field(default=None, alias='type')


class OrderDTO(BaseEntity):
    """Заказ."""
    id_field: int = Field(default=None, alias='id')
    status: str = None
    substatus: str = None
    creationDate: str = None
    currency: str = None
    itemsTotal: float
    total: float = None
    deliveryTotal: float = None
    subsidyTotal: float = None
    totalWithSubsidy: float = None
    buyerItemsTotal: float = None
    buyerTotal: float = None
    buyerItemsTotalBeforeDiscount: float = None
    buyerTotalBeforeDiscount: float = None
    paymentType: str = None
    paymentMethod: str = None
    fake: bool = None
    items: list[OrderItemDTO] = []
    subsidies: list[OrderItemSubsidyDTO] = []
    delivery: Optional[OrderDeliveryDTO] = None
    buyer: Optional[OrderBuyerDTO] = None
    notes: str = None
    taxSystem: str = None
    cancelRequested: bool = None
    expiryDate: str = None

