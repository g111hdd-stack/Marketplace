import datetime

from dataclasses import dataclass


@dataclass
class DataYaCampaigns:
    client_id: str
    campaign_id: str
    name: str
    placement_type: str


@dataclass
class DataYaReport:
    client_id: str
    campaign_id: str
    posting_number: str
    operation_type: str
    vendor_code: str
    service: str
    date: datetime.date
    cost: float


@dataclass
class DataYaOrder:
    order_date: datetime.date
    client_id: str
    sku: str
    vendor_code: str
    posting_number: str
    delivery_schema: str
    price: float
    quantities: int
    rejected: int
    returned: int
    status: str
    update_date: datetime.date
