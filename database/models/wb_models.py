from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Identity, UniqueConstraint, Boolean

from .general_models import Base


class WBMain(Base):
    """Модель таблицы wb_main_table."""
    __tablename__ = 'wb_main_table'

    id = Column(Integer, Identity(), primary_key=True)
    accrual_date = Column(Date, nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    type_of_transaction = Column(String(length=255), nullable=False)
    vendor_code = Column(String(length=255), nullable=False)
    posting_number = Column(String(length=255), nullable=False)
    delivery_schema = Column(String(length=255), nullable=False)
    sku = Column(String(length=255), nullable=False)
    sale = Column(Numeric(precision=12, scale=2), nullable=False)
    quantities = Column(Integer, nullable=False)
    commission = Column(Numeric(precision=12, scale=2), default=None, nullable=True)

    __table_args__ = (
        UniqueConstraint('accrual_date', 'type_of_transaction', 'posting_number', 'sku', name='wb_main_table_unique'),
    )


class WBCardProduct(Base):
    """Модель таблицы wb_card_product."""
    __tablename__ = 'wb_card_product'

    sku = Column(String(length=255), primary_key=True)
    vendor_code = Column(String(length=255), nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    link = Column(String(length=255), default=None, nullable=True)
    price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)
    discount_price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)


class WBStatisticCardProduct(Base):
    """Модель таблицы wb_statistic_card_product."""
    __tablename__ = 'wb_statistic_card_product'

    id = Column(Integer, Identity(), primary_key=True)
    sku = Column(String(length=255), ForeignKey('wb_card_product.sku'), nullable=False)
    date = Column(Date, nullable=False)
    open_card_count = Column(Integer, nullable=False)
    add_to_cart_count = Column(Integer, nullable=False)
    orders_count = Column(Integer, nullable=False)
    buyouts_count = Column(Integer, nullable=False)
    cancel_count = Column(Integer, nullable=False)
    orders_sum = Column(Numeric(precision=12, scale=2), nullable=False)
    price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)
    discount_price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)

    __table_args__ = (
        UniqueConstraint('sku', 'date', name='wb_statistic_card_product_unique'),
    )


class WBAdverts(Base):
    """Модель таблицы wb_adverts_table."""
    __tablename__ = 'wb_adverts_table'

    id_advert = Column(String(length=255), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    id_type = Column(Integer, ForeignKey('wb_type_advert.id_type'), nullable=False)
    id_status = Column(Integer, ForeignKey('wb_status_advert.id_status'), nullable=False)
    name_advert = Column(String(length=1000), default=None, nullable=True)
    create_time = Column(Date, nullable=False)
    change_time = Column(Date, nullable=False)
    start_time = Column(Date, nullable=False)
    end_time = Column(Date, nullable=False)


class WBTypeAdvert(Base):
    """Модель таблицы wb_type_advert."""
    __tablename__ = 'wb_type_advert'

    id_type = Column(Integer, primary_key=True)
    type = Column(String(length=255), default=None, nullable=True)


class WBStatusAdvert(Base):
    """Модель таблицы wb_status_advert."""
    __tablename__ = 'wb_status_advert'

    id_status = Column(Integer, primary_key=True)
    status = Column(String(length=255), default=None, nullable=True)


class WBStatisticAdvert(Base):
    """Модель таблицы wb_statistic_advert."""
    __tablename__ = 'wb_statistic_advert'

    id = Column(Integer, Identity(), primary_key=True)
    sku = Column(String(length=255), ForeignKey('wb_card_product.sku'), nullable=False)
    advert_id = Column(String(length=255), ForeignKey('wb_adverts_table.id_advert'), nullable=False)
    date = Column(Date, nullable=False)
    views = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    atbs = Column(Integer, nullable=False)
    orders_count = Column(Integer, nullable=False)
    shks = Column(Integer, nullable=False)
    sum_price = Column(Numeric(precision=12, scale=2), nullable=False)
    sum_cost = Column(Numeric(precision=12, scale=2), nullable=False)
    appType = Column(String(length=255), nullable=False)

    __table_args__ = (
        UniqueConstraint('sku', 'advert_id', 'date', 'appType', name='wb_statistic_advert_unique'),
    )


class WBReport(Base):
    """Модель таблицы wb_report."""
    __tablename__ = 'wb_report'

    id = Column(Integer, Identity(), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    realizationreport_id = Column(String(length=255), default=None, nullable=True)
    gi_id = Column(String(length=255), default=None, nullable=True)
    subject_name = Column(String(length=255), default=None, nullable=True)
    sku = Column(String(length=255), nullable=False)
    brand = Column(String(length=255), default=None, nullable=True)
    vendor_code = Column(String(length=255), nullable=False)
    size = Column(String(length=255), default=None, nullable=True)
    barcode = Column(String(length=255), default=None, nullable=True)
    doc_type_name = Column(String(length=255), default=None, nullable=True)
    quantity = Column(Integer, nullable=False)
    retail_price = Column(Numeric(precision=12, scale=2), nullable=False)
    retail_amount = Column(Numeric(precision=12, scale=2), nullable=False)
    sale_percent = Column(Integer, nullable=False)
    commission_percent = Column(Numeric(precision=12, scale=2), nullable=False)
    office_name = Column(String(length=255), default=None, nullable=True)
    supplier_oper_name = Column(String(length=255), nullable=False)
    order_date = Column(Date, nullable=False)
    sale_date = Column(Date, nullable=False)
    operation_date = Column(Date, nullable=False)
    shk_id = Column(String(length=255), default=None, nullable=True)
    retail_price_withdisc_rub = Column(Numeric(precision=12, scale=2), nullable=False)
    delivery_amount = Column(Integer, nullable=False)
    return_amount = Column(Integer, nullable=False)
    delivery_rub = Column(Numeric(precision=12, scale=2), nullable=False)
    gi_box_type_name = Column(String(length=255), default=None, nullable=True)
    product_discount_for_report = Column(Numeric(precision=12, scale=2), nullable=False)
    supplier_promo = Column(Numeric(precision=12, scale=2), nullable=False)
    order_id = Column(String(length=255), default=None, nullable=True)
    ppvz_spp_prc = Column(Numeric(precision=12, scale=2),  nullable=False)
    ppvz_kvw_prc_base = Column(Numeric(precision=12, scale=2), nullable=False)
    ppvz_kvw_prc = Column(Numeric(precision=12, scale=2), nullable=False)
    sup_rating_prc_up = Column(Numeric(precision=12, scale=2), nullable=False)
    is_kgvp_v2 = Column(Numeric(precision=12, scale=2), nullable=False)
    ppvz_sales_commission = Column(Numeric(precision=12, scale=2), nullable=False)
    ppvz_for_pay = Column(Numeric(precision=12, scale=2), nullable=False)
    ppvz_reward = Column(Numeric(precision=12, scale=2), nullable=False)
    acquiring_fee = Column(Numeric(precision=12, scale=2), nullable=False)
    acquiring_bank = Column(String(length=255), default=None, nullable=True)
    ppvz_vw = Column(Numeric(precision=12, scale=2), nullable=False)
    ppvz_vw_nds = Column(Numeric(precision=12, scale=2), nullable=False)
    ppvz_office_id = Column(String(length=255), default=None, nullable=True)
    ppvz_office_name = Column(String(length=255), default=None, nullable=True)
    ppvz_supplier_id = Column(String(length=255), default=None, nullable=True)
    ppvz_supplier_name = Column(String(length=255), default=None, nullable=True)
    ppvz_inn = Column(String(length=255), default=None, nullable=True)
    declaration_number = Column(String(length=255), default=None, nullable=True)
    bonus_type_name = Column(String(length=1000), default=None, nullable=True)
    sticker_id = Column(String(length=255), default=None, nullable=True)
    site_country = Column(String(length=255), default=None, nullable=True)
    penalty = Column(Numeric(precision=12, scale=2), nullable=False)
    additional_payment = Column(Numeric(precision=12, scale=2), nullable=False)
    rebill_logistic_cost = Column(Numeric(precision=12, scale=2), nullable=False)
    rebill_logistic_org = Column(String(length=255), default=None, nullable=True)
    kiz = Column(String(length=255), default=None, nullable=True)
    storage_fee = Column(Numeric(precision=12, scale=2), nullable=False)
    deduction = Column(Numeric(precision=12, scale=2), nullable=False)
    acceptance = Column(Numeric(precision=12, scale=2), nullable=False)
    posting_number = Column(String(length=255), nullable=False)


class WBTypeServices(Base):
    """Модель таблицы wb_type_services."""
    __tablename__ = 'wb_type_services'

    id = Column(Integer, Identity(), primary_key=True)
    operation_type = Column(String(length=255), nullable=False)
    service = Column(String(length=1000), default=None, nullable=True)
    type_name = Column(String(length=255), default=None, nullable=True)


class WBStorage(Base):
    """Модель таблицы wb_storage."""
    __tablename__ = 'wb_storage'

    id = Column(Integer, Identity(), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    date = Column(Date, nullable=False)
    vendor_code = Column(String(length=255), nullable=False)
    sku = Column(String(length=255), nullable=False)
    calc_type = Column(String(length=255), nullable=False)
    cost = Column(Numeric(precision=12, scale=2), nullable=False)

    __table_args__ = (
        UniqueConstraint('date', 'sku', 'calc_type', name='wb_storage_unique'),
    )


class WBOrders(Base):
    """Модель таблицы wb_orders."""
    __tablename__ = 'wb_orders'

    id = Column(Integer, Identity(), primary_key=True)
    order_date = Column(Date, nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    sku = Column(String(length=255), nullable=False)
    vendor_code = Column(String(length=255), nullable=False)
    category = Column(String(length=255), nullable=False)
    subject = Column(String(length=255), nullable=False)
    posting_number = Column(String(length=255), nullable=False)
    price = Column(Numeric(precision=12, scale=2), nullable=False)
    is_cancel = Column(Boolean, nullable=True)
    cancel_date = Column(Date, nullable=True)

    __table_args__ = (
        UniqueConstraint('order_date', 'sku', 'posting_number', name='wb_orders_unique'),
    )


class WBAcceptance(Base):
    """Модель таблицы wb_acceptance."""
    __tablename__ = 'wb_acceptance'

    id = Column(Integer, Identity(), primary_key=True)
    date = Column(Date, nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    sku = Column(String(length=255), nullable=False)
    vendor_code = Column(String(length=255), default=None, nullable=True)
    cost = Column(Numeric(precision=12, scale=2), nullable=False)

    __table_args__ = (
        UniqueConstraint('date', 'sku', name='wb_acceptance_unique'),
    )
