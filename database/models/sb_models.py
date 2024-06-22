from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Identity, Unicode
from sqlalchemy.orm import relationship

from .general_models import Base


class SbMain(Base):
    """Модель таблицы sb_main_table."""
    __tablename__ = 'sb_main_table'

    id = Column(Integer, Identity(), primary_key=True)
    accrual_date = Column(Date, nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    type_of_transaction = Column(String, nullable=False)
    vendor_code = Column(Unicode, nullable=False)
    posting_number = Column(String, nullable=False)
    delivery_schema = Column(String, nullable=False)
    sku = Column(String, nullable=False)
    sale = Column(Numeric(precision=12, scale=2), nullable=False)
    quantities = Column(Integer, nullable=False)

    client = relationship("Client", back_populates="operations_sb")


class SbStatusOrder(Base):
    """Модель таблицы sb_status_order."""
    __tablename__ = 'sb_status_order'

    field_status = Column(String(length=255), primary_key=True)
    status = Column(Unicode, default=None, nullable=True)

    order_status_field = relationship("SbOrders", back_populates="order_status")


class SbOrders(Base):
    """Модель таблицы sb_orders."""
    __tablename__ = 'sb_orders'

    posting_number = Column(String(length=255), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    field_status = Column(String(length=255), ForeignKey('sb_status_order.field_status'), nullable=False)
    date_order = Column(Date)

    client = relationship("Client", back_populates="orders_sb")
    order_status = relationship("SbStatusOrder", back_populates="order_status_field")
