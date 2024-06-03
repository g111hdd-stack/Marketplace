from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Identity, Unicode
from sqlalchemy.orm import relationship

from .general_models import Base


class YaMain(Base):
    """Модель таблицы ya_main_table."""
    __tablename__ = 'ya_main_table'

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

    client = relationship("Client", back_populates="operations_ya")


class YaCampaigns(Base):
    """Модель таблицы ya_campaigns."""
    __tablename__ = 'ya_campaigns'

    campaign_id = Column(String(length=255), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    name = Column(Unicode, nullable=False)
    placement_type = Column(Unicode, nullable=False)

    client = relationship("Client", back_populates="ya_campaigns")
