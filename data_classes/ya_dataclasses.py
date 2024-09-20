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
