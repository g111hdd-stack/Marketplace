from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Identity, UniqueConstraint, Boolean

from .general_models import Base


class YaMain(Base):
    """Модель таблицы ya_main_table."""
    __tablename__ = 'ya_main_table'

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
    bonus = Column(Numeric(precision=12, scale=2), nullable=False)

    __table_args__ = (
        UniqueConstraint('accrual_date', 'client_id', 'type_of_transaction', 'posting_number', 'sku',
                         name='wb_statistic_card_product_unique'),
    )


class YaCardProduct(Base):
    """Модель таблицы ya_card_product."""
    __tablename__ = 'ya_card_product'

    id = Column(Integer, Identity(), primary_key=True)
    sku = Column(String(length=255), nullable=False)
    vendor_code = Column(String(length=255), nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    link = Column(String(length=255), default=None, nullable=True)
    category = Column(String(length=255), default=None, nullable=True)
    price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)
    discount_price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)
    archived = Column(Boolean, default=None, nullable=True)


class YaCampaigns(Base):
    """Модель таблицы ya_campaigns."""
    __tablename__ = 'ya_campaigns'

    campaign_id = Column(String(length=255), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    name = Column(String(length=255), nullable=False)
    placement_type = Column(String(length=255), nullable=False)


class YaReport(Base):
    """Модель таблицы ya_report."""
    __tablename__ = 'ya_report'

    id = Column(Integer, Identity(), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    campaign_id = Column(String(length=255), ForeignKey('ya_campaigns.campaign_id'), nullable=True)
    date = Column(Date, nullable=False)
    posting_number = Column(String(length=255), default='', nullable=False)
    vendor_code = Column(String(length=255), default='', nullable=False)
    operation_type = Column(String(length=255), nullable=False)
    service = Column(String(length=255), default='', nullable=False)
    cost = Column(Numeric(precision=12, scale=2), nullable=False)

    __table_args__ = (
        UniqueConstraint('client_id', 'campaign_id', 'date', 'posting_number', 'vendor_code', 'operation_type', 'service',
                         name='ya_report_unique'),
    )


class YaReportShows(Base):
    """Модель таблицы ya_report_shows."""
    __tablename__ = 'ya_report_shows'

    id = Column(Integer, Identity(), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    date = Column(Date, nullable=False)
    vendor_code = Column(String(length=255), nullable=False)
    name_product = Column(String(length=255), nullable=False)
    shows = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    add_to_card = Column(Integer, nullable=False)
    orders_count = Column(Integer, nullable=False)
    cpm = Column(Numeric(precision=12, scale=2), nullable=False)
    cost = Column(Numeric(precision=12, scale=2), nullable=False)
    orders_sum = Column(Numeric(precision=12, scale=2), nullable=False)
    advert_id = Column(String(length=255), nullable=False)
    name_advert = Column(String(length=255), nullable=False)

    __table_args__ = (
        UniqueConstraint('client_id', 'date', 'vendor_code', 'advert_id', name='ya_report_shows_unique'),
    )


class YaReportConsolidated(Base):
    """Модель таблицы ya_report_consolidated."""
    __tablename__ = 'ya_report_consolidated'

    id = Column(Integer, Identity(), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    date = Column(Date, nullable=False)
    vendor_code = Column(String(length=255), nullable=False)
    name_product = Column(String(length=255), nullable=False)
    boost_shows = Column(Integer, nullable=False)
    total_shows = Column(Integer, nullable=False)
    boost_clicks = Column(Integer, nullable=False)
    total_clicks = Column(Integer, nullable=False)
    boost_add_to_card = Column(Integer, nullable=False)
    total_add_to_card = Column(Integer, nullable=False)
    boost_orders_count = Column(Integer, nullable=False)
    total_orders_count = Column(Integer, nullable=False)
    boost_orders_delivered_count = Column(Integer, nullable=False)
    total_orders_delivered_count = Column(Integer, nullable=False)
    cost = Column(Numeric(precision=12, scale=2), nullable=False)
    bonus_cost = Column(Numeric(precision=12, scale=2), nullable=False)
    average_cost = Column(Numeric(precision=12, scale=2), nullable=False)
    boost_revenue_ratio_cost = Column(Numeric(precision=12, scale=2), nullable=False)
    boost_orders_delivered_sum = Column(Numeric(precision=12, scale=2), nullable=False)
    total_orders_delivered_sum = Column(Numeric(precision=12, scale=2), nullable=False)
    revenue_ratio_boost_total = Column(Numeric(precision=12, scale=2), nullable=False)
    advert_id = Column(String(length=255), nullable=False)
    name_advert = Column(String(length=255), nullable=False)

    __table_args__ = (
        UniqueConstraint('client_id', 'date', 'vendor_code', 'advert_id', name='ya_report_consolidated_unique'),
    )


class YaReportShelf(Base):
    """Модель таблицы ya_report_shelf."""
    __tablename__ = 'ya_report_shelf'

    id = Column(Integer, Identity(), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    date = Column(Date, nullable=False)
    advert_id = Column(String(length=255), nullable=False)
    name_advert = Column(String(length=255), nullable=False)
    category = Column(String(length=255), nullable=False)
    shows = Column(Integer, nullable=False)
    coverage = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    ctr = Column(Numeric(precision=6, scale=2), nullable=False)
    shows_frequency = Column(Numeric(precision=6, scale=2), nullable=False)
    add_to_card = Column(Integer, nullable=False)
    orders_count = Column(Integer, nullable=False)
    orders_conversion = Column(Numeric(precision=6, scale=2), nullable=False)
    order_sum = Column(Numeric(precision=14, scale=2), nullable=False)
    cpo = Column(Numeric(precision=12, scale=2), nullable=False)
    average_cost_per_mille = Column(Numeric(precision=12, scale=2), nullable=False)
    cost = Column(Numeric(precision=14, scale=2), nullable=False)
    cpm = Column(Numeric(precision=12, scale=2), nullable=False)
    cost_ratio_revenue = Column(Numeric(precision=6, scale=2), nullable=False)

    __table_args__ = (
        UniqueConstraint('client_id', 'date', 'advert_id', 'category', name='ya_report_shelf_unique'),
    )


class YaAdvertCost(Base):
    """Модель таблицы ya_advert_cost."""
    __tablename__ = 'ya_advert_cost'

    id = Column(Integer, Identity(), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    date = Column(Date, nullable=False)
    advert_id = Column(String(length=255), nullable=False)
    name_advert = Column(String(length=255), nullable=False)
    type_advert = Column(String(length=255), nullable=False)
    cost = Column(Numeric(precision=14, scale=2), nullable=False)
    bonus_deducted = Column(Numeric(precision=14, scale=2), nullable=False)

    __table_args__ = (
        UniqueConstraint('client_id', 'date', 'advert_id', 'type_advert', name='ya_advert_cost_unique'),
    )


class YaTypeReport(Base):
    """Модель таблицы ya_type_services."""
    __tablename__ = 'ya_type_services'

    id = Column(Integer, Identity(), primary_key=True)
    operation_type = Column(String(length=255), nullable=False)
    service = Column(String(length=255), default='', nullable=False)
    type_name = Column(String(length=255), default='new', nullable=False)


class YaOrders(Base):
    """Модель таблицы ya_orders."""
    __tablename__ = 'ya_orders'

    id = Column(Integer, Identity(), primary_key=True)
    order_date = Column(Date, nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    sku = Column(String(length=255), nullable=False)
    vendor_code = Column(String(length=255), nullable=False)
    posting_number = Column(String(length=255), nullable=False)
    delivery_schema = Column(String(length=255), nullable=False)
    quantities = (Column(Integer, nullable=False))
    rejected = (Column(Integer, nullable=False))
    returned = (Column(Integer, nullable=False))
    price = Column(Numeric(precision=12, scale=2), nullable=False)
    bonus = Column(Numeric(precision=12, scale=2), nullable=False)
    status = Column(String(length=255), nullable=False)
    update_date = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint('order_date', 'sku', 'posting_number', name='ya_orders_unique'),
    )


class YaStock(Base):
    """Модель таблицы ya_stocks."""
    __tablename__ = 'ya_stocks'

    id = Column(Integer, Identity(), primary_key=True)
    date = Column(Date, nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    campaign_id = Column(String(length=255), nullable=False)
    vendor_code = Column(String(length=255), nullable=False)
    size = Column(String(length=255), nullable=False)
    warehouse = Column(String(length=255), nullable=False)
    quantity = Column(Integer, nullable=False)
    type = Column(String(length=255), nullable=False)

    __table_args__ = (
        UniqueConstraint('client_id', 'date', 'campaign_id', 'vendor_code', 'size', 'warehouse', 'type',
                         name='ya_stocks_unique'),
    )
