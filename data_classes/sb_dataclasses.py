import datetime

from dataclasses import dataclass


@dataclass
class DataSbOrders:
    posting_number: str
    client_id: str
    field_status: str
    date_order: datetime.date
