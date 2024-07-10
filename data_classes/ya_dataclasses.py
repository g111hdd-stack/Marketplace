from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DataYaCampaigns:
    client_id: str
    campaign_id: str
    name: str
    placement_type: str


@dataclass
class DataYaReport:
    client_id: Optional[str] = None
    campaign_id: Optional[str] = None
    posting_number: Optional[str] = None
    application_number: Optional[str] = None
    vendor_code: Optional[str] = None
    service: Optional[str] = None
    accrual_date: Optional[datetime.date] = None
    cost: Optional[float] = None
