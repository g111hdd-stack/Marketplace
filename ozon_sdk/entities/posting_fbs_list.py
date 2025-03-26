from datetime import datetime
from typing import Optional

from .picking import Picking
from .base import BaseEntity


class PostingFBSlistAddressee(BaseEntity):
    """Контактные данные получателя."""
    name: str = None
    phone: str = None


class PostingFBSListAnalyticsData(BaseEntity):
    """Данные аналитики."""
    city: str = None
    delivery_date_begin: datetime = None
    delivery_date_end: datetime = None
    delivery_type: str = None
    is_legal: bool = None
    is_premium: bool = None
    payment_type_group_name: str = None
    region: str = None
    tpl_provider: str = None
    tpl_provider_id: int = None
    warehouse: str = None
    warehouse_id: int = None


class PostingFBSListBarcodes(BaseEntity):
    """Штрихкоды отправления."""
    lower_barcode: str = None
    upper_barcode: str = None


class PostingFBSListCancellation(BaseEntity):
    """Информация об отмене."""
    affect_cancellation_rating: bool = None
    cancel_reason: str = None
    cancel_reason_id: int = None
    cancellation_initiator: str = None
    cancellation_type: str = None
    cancelled_after_ship: bool = None


class PostingFBSListCustomerAddress(BaseEntity):
    """"Информация об адресе доставки."""
    address_tail: str = None
    city: str = None
    comment: str = None
    country: str = None
    district: str = None
    latitude: float = None
    longitude: float = None
    provider_pvz_code: str = None
    pvz_code: int = None
    region: str = None
    zip_code: str = None


class PostingFBSListCustomer(BaseEntity):
    """Данные о покупателе."""
    address: Optional[PostingFBSListCustomerAddress] = None
    customer_email: str = None
    customer_id: int = None
    name: str = None
    phone: str = None


class PostingFBSListDeliveryMethod(BaseEntity):
    """Метод доставки."""
    id: int = None
    name: str = None
    tpl_provider: str = None
    tpl_provider_id: int = None
    warehouse: str = None
    warehouse_id: int = None


class PostingFBSListFinancialDataProduct(BaseEntity):
    """Информация о товаре в заказе"""
    actions: list[str] = []
    currency_code: str = None
    commission_amount: float = None
    commission_percent: float = None
    commissions_currency_code: str = None
    old_price: float = None
    payout: float = None
    picking: Optional[Picking] = None
    price: float = None
    product_id: int = None
    quantity: int = None
    total_discount_percent: float = None
    total_discount_value: float = None


class PostingFBSListFinancialData(BaseEntity):
    """Данные о стоимости товара, размере скидки, выплате и комиссии."""
    cluster_from: str = None
    cluster_to: str = None
    products: list[PostingFBSListFinancialDataProduct] = []


class PostingFBSListProduct(BaseEntity):
    """Товар в отправлении."""
    mandatory_mark: list[str] = []
    name: str = None
    offer_id: str = None
    price: str = None
    quantity: int = None
    sku: int = None
    currency_code: str = None


class PostingFBSListRequirements(BaseEntity):
    """
        Cписок продуктов, для которых нужно передать страну-изготовителя, номер грузовой таможенной декларации (ГТД),
        регистрационный номер партии товара (РНПТ) или маркировку «Честный ЗНАК», чтобы перевести отправление в следующий статус.
    """
    products_requiring_gtd: list[int] = []
    products_requiring_country: list[int] = []
    products_requiring_mandatory_mark: list[int] = []
    products_requiring_jw_uin: list[int] = []
    products_requiring_rnpt: list[int] = []


class PostingFBSListPosting(BaseEntity):
    """Информация об отправлении."""
    addressee: Optional[PostingFBSlistAddressee] = None
    analytics_data: Optional[PostingFBSListAnalyticsData] = None
    available_actions: list[str] = []
    barcodes: Optional[PostingFBSListBarcodes] = None
    cancellation: Optional[PostingFBSListCancellation] = None
    customer: Optional[PostingFBSListCustomer] = None
    delivering_date: Optional[datetime] = None
    delivery_method: Optional[PostingFBSListDeliveryMethod] = None
    financial_data: Optional[PostingFBSListFinancialData] = None
    in_process_at: datetime = None
    is_express: bool = None
    is_multibox: bool = None
    multi_box_qty: int = None
    order_id: int = None
    order_number: str = None
    parent_posting_number: str = None
    posting_number: str = None
    products: list[PostingFBSListProduct] = []
    prr_option: str = None
    requirements: Optional[PostingFBSListRequirements] = None
    shipment_date: datetime = None
    status: str = None
    substatus: str = None
    tpl_integration_type: str = None
    tracking_number: str = None


class PostingFBSList(BaseEntity):
    """Информация об отправлении."""
    has_next: bool
    postings: list[PostingFBSListPosting] = []
