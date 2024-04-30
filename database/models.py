from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, MetaData, Identity, Unicode
from sqlalchemy.orm import relationship, declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Client(Base):
    """Модель таблицы clients"""
    __tablename__ = 'clients'

    client_id = Column(String(length=255), primary_key=True)
    api_key = Column(String(length=255), unique=True, nullable=False)
    marketplace = Column(String, nullable=False)
    name_company = Column(Unicode, nullable=False)

    operations_oz = relationship("OzMain", back_populates="client")
    operations_wb = relationship("WBMain", back_populates="client")


class OzMain(Base):
    """Модель таблицы oz_main_table"""
    __tablename__ = 'oz_main_table'

    id = Column(Integer, Identity(), primary_key=True)
    accrual_date = Column(Date, nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    type_of_transaction = Column(String, nullable=False)
    vendor_cod = Column(Unicode, nullable=False)
    posting_number = Column(String, nullable=False)
    delivery_schema = Column(String, nullable=False)
    sku = Column(String, nullable=False)
    sale = Column(Numeric(precision=12, scale=2), nullable=False)
    quantities = Column(Integer, nullable=False)

    client = relationship("Client", back_populates="operations_oz")


class WBMain(Base):
    """Модель таблицы wb_main_table"""
    __tablename__ = 'wb_main_table'

    id = Column(Integer, Identity(), primary_key=True)
    accrual_date = Column(Date, nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    type_of_transaction = Column(String, nullable=False)
    vendor_cod = Column(Unicode, nullable=False)
    posting_number = Column(String, nullable=False)
    delivery_schema = Column(String, nullable=False)
    sku = Column(String, nullable=False)
    sale = Column(Numeric(precision=12, scale=2), nullable=False)
    quantities = Column(Integer, nullable=False)

    client = relationship("Client", back_populates="operations_wb")
