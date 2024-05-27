import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ConnectionSettings:
    server: str
    database: str
    username: str
    password: str
    driver: str
    timeout: int


@dataclass
class DataOperation:
    client_id: str
    accrual_date: datetime.date
    type_of_transaction: str
    vendor_code: str
    delivery_schema: str
    posting_number: str
    sku: str
    sale: float
    quantities: int


@dataclass
class DataWBStatisticAdvert:
    client_id: str
    date: datetime.datetime
    advert_id: int
    views: int
    clicks: int
    ctr: float
    cpc: float
    sum_cost: float
    atbs: int
    orders_count: int
    shks: int
    sum_price: float
    nm_id: str
    app_type: str


@dataclass
class DataWBStatisticCardProduct:
    sku: str
    vendor_code: str
    client_id: str
    category: str
    brand: str
    link: str
    date: datetime.date
    open_card_count: int
    add_to_cart_count: int
    orders_count: int
    add_to_cart_percent: float
    cart_to_order_percent: float


@dataclass
class DataWBAdvert:
    id_advert: int
    id_type: int
    id_status: int
    name_advert: str
    create_time: datetime.date
    change_time: datetime.date
    start_time: datetime.date
    end_time: datetime.date


@dataclass
class DataWBProductCard:
    sku: str
    client_id: str
    vendor_code: str
    price: float
    discount_price: float


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
