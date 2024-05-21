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
    sum_field: float
    atbs: int
    orders: int
    cr: float
    shks: int
    sum_price: float
    name: str
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
    type_field: str
    id_status: int
    status: str
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
