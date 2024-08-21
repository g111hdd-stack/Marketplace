from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Identity, Unicode
from sqlalchemy.orm import relationship

from .general_models import Base


class OzMain(Base):
    """Модель таблицы oz_main_table."""
    __tablename__ = 'oz_main_table'

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
    commission = Column(Numeric(precision=12, scale=2), nullable=False)
    cost_last_mile = Column(Numeric(precision=12, scale=2), nullable=False)
    cost_logistic = Column(Numeric(precision=12, scale=2), nullable=False)

    client = relationship("Client", back_populates="operations_oz")


class OzPerformance(Base):
    """Модель таблицы date."""
    __tablename__ = 'oz_performance'

    performance_id = Column(String(length=255), primary_key=True, nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    client_secret = Column(String(length=1000), unique=True, nullable=False)

    client = relationship("Client", back_populates="oz_performance")


class OzCardProduct(Base):
    """Модель таблицы oz_card_product."""
    __tablename__ = 'oz_card_product'

    sku = Column(String(length=255), primary_key=True, nullable=False)
    vendor_code = Column(Unicode, nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    category = Column(Unicode, default=None, nullable=True)
    brand = Column(Unicode, default=None, nullable=True)
    link = Column(Unicode, default=None, nullable=True)
    price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)
    discount_price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)

    client = relationship("Client", back_populates="card_product_oz")
    statistic_card_product = relationship("OzStatisticCardProduct", back_populates="card_product")
    statistic_advert = relationship("OzStatisticAdvert", back_populates="card_product")


class OzStatisticCardProduct(Base):
    """Модель таблицы oz_statistic_card_product."""
    __tablename__ = 'oz_statistic_card_product'

    id = Column(Integer, Identity(), primary_key=True)
    sku = Column(String(length=255), ForeignKey('oz_card_product.sku'), nullable=False)
    date = Column(Date, nullable=False)
    view_search = Column(Integer, nullable=False)
    view_card = Column(Integer, nullable=False)
    add_to_cart_from_search_count = Column(Integer, nullable=False)
    add_to_cart_from_card_count = Column(Integer, nullable=False)
    orders_count = Column(Integer, nullable=False)
    add_to_cart_from_card_percent = Column(Numeric(precision=12, scale=2), nullable=False)
    add_to_cart_from_search_percent = Column(Numeric(precision=12, scale=2), nullable=False)
    price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)
    discount_price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)

    card_product = relationship("OzCardProduct", back_populates="statistic_card_product")


class OzTypeAdvert(Base):
    """Модель таблицы oz_type_advert."""
    __tablename__ = 'oz_type_advert'

    field_type = Column(String(length=255), primary_key=True)
    type = Column(Unicode, default=None, nullable=True)

    advert_type_field = relationship("OzAdverts", back_populates="advert_type")


class OzStatusAdvert(Base):
    """Модель таблицы oz_status_advert."""
    __tablename__ = 'oz_status_advert'

    field_status = Column(String(length=255), primary_key=True)
    status = Column(Unicode, default=None, nullable=True)

    advert_status_field = relationship("OzAdverts", back_populates="advert_status")


class OzAdverts(Base):
    """Модель таблицы oz_adverts_table."""
    __tablename__ = 'oz_adverts_table'

    id_advert = Column(String(length=255), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    field_type = Column(String(length=255), ForeignKey('oz_type_advert.field_type'), nullable=False)
    field_status = Column(String(length=255), ForeignKey('oz_status_advert.field_status'), nullable=False)
    name_advert = Column(Unicode, default=None, nullable=True)
    create_time = Column(Date)
    change_time = Column(Date)
    start_time = Column(Date, default=None, nullable=True)
    end_time = Column(Date, default=None, nullable=True)

    advert_type = relationship("OzTypeAdvert", back_populates="advert_type_field")
    advert_status = relationship("OzStatusAdvert", back_populates="advert_status_field")
    client = relationship("Client", back_populates="adverts_oz")


class OzStatisticAdvert(Base):
    """Модель таблицы oz_statistic_advert."""
    __tablename__ = 'oz_statistic_advert'

    id = Column(Integer, Identity(), primary_key=True)
    sku = Column(String(length=255), ForeignKey('oz_card_product.sku'), nullable=False)
    advert_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    views = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    cpc = Column(Numeric(precision=12, scale=2), nullable=False)
    orders_count = Column(Integer, nullable=False)
    sum_price = Column(Numeric(precision=12, scale=2), nullable=False)
    sum_cost = Column(Numeric(precision=12, scale=2), nullable=False)

    card_product = relationship("OzCardProduct", back_populates="statistic_advert")


class OzAdvertDailyBudget(Base):
    """Модель таблицы oz_advert_daily_budget."""
    __tablename__ = 'oz_advert_daily_budget'

    id = Column(Integer, Identity(), primary_key=True)
    date = Column(Date, nullable=False)
    advert_id = Column(String, nullable=False)
    daily_budget = Column(Numeric(precision=12, scale=2), nullable=False)


class OzReport(Base):
    """Модель таблицы oz_report."""
    __tablename__ = 'oz_report'

    id = Column(Integer, Identity(), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=True)
    posting_number = Column(String(length=255), nullable=True)
    vendor_code = Column(Unicode, nullable=True)
    service = Column(Unicode, nullable=True)
    operation_date = Column(Date, nullable=True)
    cost = Column(Numeric(precision=12, scale=2), nullable=False)

    client = relationship("Client", back_populates="report_oz")


class OzStorage(Base):
    """Модель таблицы oz_storage."""
    __tablename__ = 'oz_storage'

    id = Column(Integer, Identity(), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    date = Column(Date, nullable=False)
    vendor_code = Column(Unicode, nullable=False)
    sku = Column(String(length=255), nullable=False)
    cost = Column(Numeric(precision=12, scale=2), default=None, nullable=False)

    client = relationship("Client", back_populates="storage_oz")


class OzServices(Base):
    """Модель таблицы oz_services."""
    __tablename__ = 'oz_services'

    id = Column(Integer, Identity(), primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    date = Column(Date, nullable=False)
    operation_type = Column(Unicode, nullable=False)
    operation_type_name = Column(Unicode, nullable=True)
    vendor_code = Column(Unicode, nullable=True)
    sku = Column(String(length=255), nullable=True)
    posting_number = Column(String(length=255), nullable=True)
    service = Column(Unicode, nullable=True)
    cost = Column(Numeric(precision=12, scale=2), default=None, nullable=False)

    client = relationship("Client", back_populates="services_oz")


class OzTypeServices(Base):
    """Модель таблицы oz_type_services."""
    __tablename__ = 'oz_type_services'

    id = Column(Integer, Identity(), primary_key=True)
    operation_type = Column(Unicode, nullable=False)
    service = Column(Unicode, nullable=True)
    type_name = Column(Unicode, nullable=True)
