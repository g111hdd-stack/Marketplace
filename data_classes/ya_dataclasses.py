import datetime

from dataclasses import dataclass
from typing import Optional


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
class DataYaReportShows:
    client_id: str
    date: datetime.date
    vendor_code: str
    name_product: str
    shows: int
    clicks: int
    add_to_card: int
    orders_count: int
    cpm: float
    cost: float
    orders_sum: float
    advert_id: str
    name_advert: str


@dataclass
class DataYaReportConsolidated:
    client_id: str
    date: datetime.date
    vendor_code: str
    name_product: str
    boost_shows: int
    total_shows: int
    boost_clicks: int
    total_clicks: int
    boost_add_to_card: int
    total_add_to_card: int
    boost_orders_count: int
    total_orders_count: int
    boost_orders_delivered_count: int
    total_orders_delivered_count: int
    cost: float
    bonus_cost: float
    average_cost: float
    boost_cost_ratio_revenue: float
    boost_orders_delivered_sum: float
    total_orders_delivered_sum: float
    boost_revenue_ratio_total: float
    advert_id: str
    name_advert: str


@dataclass
class DataYaReportShelf:
    client_id: str
    date: datetime.date
    advert_id: str
    name_advert: str
    category: str
    shows: int
    coverage: int
    clicks: int
    ctr: float
    shows_frequency: float
    add_to_card: int
    orders_count: int
    orders_conversion: float
    order_sum: float
    cpo: float
    average_cost_per_mille: float
    cost: float
    cpm: float
    cost_ratio_revenue: float


@dataclass
class DataYaAdvertCost:
    client_id: str
    date: datetime.date
    advert_id: str
    name_advert: str
    cost: float
    bonus_deducted: float
    type_advert: Optional[str] = None


@dataclass
class DataYaOrder:
    order_date: datetime.date
    client_id: str
    sku: str
    vendor_code: str
    posting_number: str
    delivery_schema: str
    price: float
    bonus: float
    quantities: int
    rejected: int
    returned: int
    status: str
    update_date: datetime.date


@dataclass
class DataYaStock:
    date: datetime.date
    client_id: str
    campaign_id: str
    vendor_code: str
    size: str
    warehouse: str
    quantity: int
    type: str


@dataclass
class DataYaCardProduct:
    sku: Optional[str]
    category: Optional[str]
    archived: bool
    vendor_code: str
    client_id: str
    link: str
    price: float
    discount_price: float
