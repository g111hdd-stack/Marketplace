import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class DataOzProductCard:
    sku: str
    client_id: str
    vendor_code: str
    brand: str
    category: str
    link: str
    price: float
    discount_price: float


@dataclass
class DataOzStatisticCardProduct:
    sku: str
    date: datetime.date
    orders_count: int
    add_to_cart_from_search_count: int
    add_to_cart_from_card_count: int
    view_search: int
    view_card: int
    add_to_cart_from_search_percent: float
    add_to_cart_from_card_percent: float


@dataclass
class DataOzAdvert:
    id_advert: int
    field_type: str
    field_status: str
    name_advert: str
    create_time: datetime.date
    change_time: datetime.date
    start_time: Optional[datetime.date] = None
    end_time: Optional[datetime.date] = None


@dataclass
class DataOzStatisticAdvert:
    client_id: str
    date: datetime.date
    sku: str
    advert_id: int
    views: int
    clicks: int
    cpc: float
    sum_cost: float
    orders_count: int
    sum_price: float


@dataclass
class DataOzReport:
    client_id: Optional[str] = None
    posting_number: Optional[str] = None
    sku: Optional[str] = None
    service: Optional[str] = None
    operation_date: Optional[datetime.date] = None
    cost: Optional[float] = None
