import datetime

from dataclasses import dataclass


@dataclass
class DataWBCardProduct:
    sku: str
    vendor_code: str
    client_id: str
    link: str
    price: float
    discount_price: float


@dataclass
class DataWBStatisticCardProduct:
    sku: str
    vendor_code: str
    client_id: str
    date: datetime.date
    open_card_count: int
    add_to_cart_count: int
    orders_count: int
    buyouts_count: int
    cancel_count: int
    orders_sum: float


@dataclass
class DataWBAdvert:
    id_advert: str
    id_type: int
    id_status: int
    name_advert: str
    create_time: datetime.date
    change_time: datetime.date
    start_time: datetime.date
    end_time: datetime.date


@dataclass
class DataWBStatisticAdvert:
    client_id: str
    sku: str
    advert_id: str
    date: datetime.date
    views: int
    clicks: int
    atbs: int
    orders_count: int
    shks: int
    sum_price: float
    sum_cost: float
    app_type: str


@dataclass
class DataWBReport:
    realizationreport_id: str
    gi_id: str
    subject_name: str
    sku: str
    brand: str
    vendor_code: str
    size: str
    barcode: str
    doc_type_name: str
    quantity: int
    retail_price: float
    retail_amount: float
    sale_percent: int
    commission_percent: float
    office_name: str
    supplier_oper_name: str
    order_date: datetime.date
    sale_date: datetime.date
    operation_date: datetime.date
    shk_id: str
    retail_price_withdisc_rub: float
    delivery_amount: int
    return_amount: int
    delivery_rub: float
    gi_box_type_name: str
    product_discount_for_report: float
    supplier_promo: float
    order_id: str
    ppvz_spp_prc: float
    ppvz_kvw_prc_base: float
    ppvz_kvw_prc: float
    sup_rating_prc_up: float
    is_kgvp_v2: float
    ppvz_sales_commission: float
    ppvz_for_pay: float
    ppvz_reward: float
    acquiring_fee: float
    acquiring_bank: str
    ppvz_vw: float
    ppvz_vw_nds: float
    ppvz_office_id: str
    ppvz_office_name: str
    ppvz_supplier_id: str
    ppvz_supplier_name: str
    ppvz_inn: str
    declaration_number: str
    bonus_type_name: str
    sticker_id: str
    site_country: str
    penalty: float
    additional_payment: float
    rebill_logistic_cost: float
    rebill_logistic_org: str
    kiz: str
    storage_fee: float
    deduction: float
    acceptance: float
    posting_number: str


@dataclass
class DataWBStorage:
    client_id: str
    date: datetime.date
    vendor_code: str
    sku: str
    calc_type: str
    cost: float


@dataclass
class DataWBAcceptance:
    client_id: str
    date: datetime.date
    sku: str
    cost: float


@dataclass
class DataWBOrder:
    order_date: datetime.date
    client_id: str
    sku: str
    vendor_code: str
    category: str
    subject: str
    posting_number: str
    price: float
    is_cancel: bool
    cancel_date: datetime.date
    warehouse: str
    warehouse_type: str
    country: str
    oblast: str
    region: str


@dataclass
class DataWBStock:
    date: datetime.date
    client_id: str
    sku: str
    vendor_code: str
    size: str
    category: str
    subject: str
    warehouse: str
    quantity_warehouse: int
    quantity_to_client: int
    quantity_from_client: int
