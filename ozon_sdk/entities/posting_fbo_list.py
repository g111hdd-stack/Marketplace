from datetime import datetime
from typing import Optional

from .picking import Picking
from .services import Services
from .base import BaseEntity


class PostingFBOListAdditionalData(BaseEntity):
    """additional_data"""
    key: str = None
    value: str = None


class PostingFBOListAnalyticsData(BaseEntity):
    """Данные аналитики."""
    city: str = None
    delivery_type: str = None
    is_legal: bool = None
    is_premium: bool = None
    payment_type_group_name: str = None
    warehouse: str = None
    warehouse_id: int = None


class PostingFBOListFinancialDataProduct(BaseEntity):
    """Информация о товаре в заказе"""
    actions: list[str] = []
    currency_code: str = None
    commission_amount: float = None
    commission_percent: float = None
    commissions_currency_code: str = None
    item_services: Optional[Services] = None
    old_price: float = None
    payout: float = None
    picking: Optional[Picking] = None
    price: float = None
    product_id: int = None
    quantity: int = None
    total_discount_percent: float = None
    total_discount_value: float = None


class PostingFBOListProduct(BaseEntity):
    """Товар в отправлении."""
    digital_codes: list[str] = []
    name: str = None
    offer_id: str = None
    currency_code: str = None
    price: str = None
    quantity: int = None
    sku: int = None


class PostingFBOListFinanciallData(BaseEntity):
    """Финансовые данные."""
    posting_services: Optional[Services] = None
    cluster_from: str
    cluster_to: str
    products: Optional[PostingFBOListFinancialDataProduct] = None


class PostingFBOList(BaseEntity):
    """Информация об отправлении."""
    additional_data: list[PostingFBOListAdditionalData] = []
    analytics_data: Optional[PostingFBOListAnalyticsData] = None
    cancel_reason_id: int
    created_at: datetime
    financial_data: Optional[PostingFBOListFinanciallData] = None
    in_process_at: datetime
    order_id: int
    order_number: str
    posting_number: str
    products: list[PostingFBOListProduct] = []
    status: str
