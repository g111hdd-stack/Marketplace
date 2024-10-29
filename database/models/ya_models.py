from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Identity, UniqueConstraint

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

    __table_args__ = (
        UniqueConstraint('accrual_date', 'client_id', 'type_of_transaction', 'posting_number', 'sku',
                         name='wb_statistic_card_product_unique'),
    )


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
    campaign_id = Column(String(length=255), ForeignKey('ya_campaigns.campaign_id'), nullable=False)
    date = Column(Date, nullable=False)
    posting_number = Column(String(length=255), default='', nullable=False)
    vendor_code = Column(String(length=255), default='', nullable=False)
    operation_type = Column(String(length=255), nullable=False)
    service = Column(String(length=255), default='', nullable=False)
    cost = Column(Numeric(precision=12, scale=2), nullable=False)

    __table_args__ = (
        UniqueConstraint('client_id', 'campaign_id', 'date', 'posting_number', 'vendor_code', 'operation_type', 'service',
                         name='wb_statistic_card_product_unique'),
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
    status = Column(String(length=255), nullable=False)
    update_date = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint('order_date', 'sku', 'posting_number', name='ya_orders_unique'),
    )
