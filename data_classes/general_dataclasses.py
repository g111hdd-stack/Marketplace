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
    commission: Optional[float] = None
    cost_last_mile: Optional[float] = None
    cost_logistic: Optional[float] = None
