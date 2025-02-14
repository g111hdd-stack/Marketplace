from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Identity, UniqueConstraint

from .general_models import Base


class SbMain(Base):
    """Модель таблицы sb_main_table."""
    __tablename__ = 'sb_main_table'

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
        UniqueConstraint('accrual_date', 'type_of_transaction', 'posting_number', 'sku', name='sb_main_table_unique'),
    )


class SbOrders(Base):
    """Модель таблицы sb_orders."""
    __tablename__ = 'sb_orders'

    posting_number = Column(String(length=255), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    field_status = Column(String(length=255), ForeignKey('sb_status_order.field_status'), nullable=False)
    date_order = Column(Date, nullable=False)


class SbStatusOrder(Base):
    """Модель таблицы sb_status_order."""
    __tablename__ = 'sb_status_order'

    field_status = Column(String(length=255), primary_key=True)
    status = Column(String, default=None, nullable=True)
