import datetime
from dataclasses import dataclass
from typing import Optional


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
    buyouts_count: int
    buyouts_last_30days_percent: Optional[float] = None


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
class DataWBReport:
    realizationreport_id: str = None
    gi_id: str = None
    subject_name: str = None
    sku: str = None
    brand: str = None
    vendor_code: str = None
    size: str = None
    barcode: str = None
    doc_type_name: str = None
    quantity: int = None
    retail_price: float = None
    retail_amount: float = None
    sale_percent: int = None
    commission_percent: float = None
    office_name: str = None
    supplier_oper_name: str = None
    order_date: datetime.date = None
    sale_date: datetime.date = None
    operation_date: datetime.date = None
    shk_id: str = None
    retail_price_withdisc_rub: float = None
    delivery_amount: int = None
    return_amount: int = None
    delivery_rub: float = None
    gi_box_type_name: str = None
    product_discount_for_report: float = None
    supplier_promo: float = None
    order_id: str = None
    ppvz_spp_prc: float = None
    ppvz_kvw_prc_base: float = None
    ppvz_kvw_prc: float = None
    sup_rating_prc_up: float = None
    is_kgvp_v2: float = None
    ppvz_sales_commission: float = None
    ppvz_for_pay: float = None
    ppvz_reward: float = None
    acquiring_fee: float = None
    acquiring_bank: str = None
    ppvz_vw: float = None
    ppvz_vw_nds: float = None
    ppvz_office_id: str = None
    ppvz_office_name: str = None
    ppvz_supplier_id: str = None
    ppvz_supplier_name: str = None
    ppvz_inn: str = None
    declaration_number: str = None
    bonus_type_name: str = None
    sticker_id: str = None
    site_country: str = None
    penalty: float = None
    additional_payment: float = None
    rebill_logistic_cost: float = None
    rebill_logistic_org: str = None
    kiz: str = None
    storage_fee: float = None
    deduction: float = None
    acceptance: float = None
    posting_number: str = None


@dataclass
class DataWBStorage:
    client_id: str
    date: datetime.datetime
    vendor_code: str
    sku: str
    calc_type: str
    cost: float
