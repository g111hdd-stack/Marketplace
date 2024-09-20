import datetime

from typing import Optional
from dataclasses import dataclass


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
    commission: Optional[float] = None


@dataclass
class DataOrder:
    client_id: str
    order_date: datetime.date
    sku: str
    vendor_code: str
    posting_number: str
    price: float
    category: Optional[str] = None
    subject: Optional[str] = None


@dataclass
class DataCostPrice:
    month_date: int
    year_date: int
    vendor_code: str
    cost: float


@dataclass
class DataSelfPurchase:
    client_id: str
    order_date: datetime.date
    accrual_date: datetime.date
    vendor_code: str
    quantities: int
    price: float
