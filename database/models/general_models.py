from sqlalchemy import Column, String, Date, MetaData, Unicode, Integer, Identity, Numeric
from sqlalchemy.orm import relationship, declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Client(Base):
    """Модель таблицы clients."""
    __tablename__ = 'clients'

    client_id = Column(String(length=255), primary_key=True)
    api_key = Column(String(length=1000), nullable=False)
    marketplace = Column(Unicode, nullable=False)
    name_company = Column(Unicode, nullable=False)
    entrepreneur = Column(Unicode, nullable=True)

    operations_oz = relationship("OzMain", back_populates="client")
    operations_wb = relationship("WBMain", back_populates="client")
    operations_ya = relationship("YaMain", back_populates="client")
    operations_sb = relationship("SbMain", back_populates="client")
    card_product_wb = relationship("WBCardProduct", back_populates="client")
    adverts_wb = relationship("WBAdverts", back_populates="client")
    oz_performance = relationship("OzPerformance", back_populates="client")
    card_product_oz = relationship("OzCardProduct", back_populates="client")
    adverts_oz = relationship("OzAdverts", back_populates="client")
    ya_campaigns = relationship("YaCampaigns", back_populates="client")
    report_wb = relationship("WBReport", back_populates="client")
    orders_sb = relationship("SbOrders", back_populates="client")
    report_ya = relationship("YaReport", back_populates="client")
    report_oz = relationship("OzReport", back_populates="client")
    storage_wb = relationship("WBStorage", back_populates="client")
    storage_oz = relationship("OzStorage", back_populates="client")
    services_oz = relationship("OzServices", back_populates="client")


class CostPrice(Base):
    """Модель таблицы cost_price."""
    __tablename__ = 'cost_price'

    id = Column(Integer, Identity(), primary_key=True)
    month_date = Column(Integer, nullable=True)
    year_date = Column(Integer, nullable=True)
    vendor_code = Column(Unicode, nullable=True)
    cost = Column(Numeric(precision=12, scale=2), nullable=True)
