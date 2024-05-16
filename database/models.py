from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, MetaData, Identity, Unicode, DateTime
from sqlalchemy.orm import relationship, declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Client(Base):
    """Модель таблицы clients."""
    __tablename__ = 'clients'

    client_id = Column(String(length=255), primary_key=True)
    api_key = Column(String(length=1000), unique=True, nullable=False)
    marketplace = Column(String, nullable=False)
    name_company = Column(Unicode, nullable=False)
    entrepreneur = Column(Unicode, nullable=True)

    operations_oz = relationship("OzMain", back_populates="client")
    operations_wb = relationship("WBMain", back_populates="client")
    operations_ya = relationship("YaMain", back_populates="client")
    card_product_wb = relationship("WBCardProduct", back_populates="client")
    adverts_wb = relationship("WBAdverts", back_populates="client")


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

    client = relationship("Client", back_populates="operations_oz")


class WBMain(Base):
    """Модель таблицы wb_main_table."""
    __tablename__ = 'wb_main_table'

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

    client = relationship("Client", back_populates="operations_wb")


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


class WBCardProduct(Base):
    """Модель таблицы wb_card_product."""
    __tablename__ = 'wb_card_product'

    sku = Column(String(length=255), primary_key=True, nullable=False)
    vendor_code = Column(Unicode, nullable=False)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    category = Column(Unicode, default=None, nullable=True)
    brand = Column(Unicode, default=None, nullable=True)
    link = Column(Unicode, default=None, nullable=True)
    price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)
    discount_price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)

    client = relationship("Client", back_populates="card_product_wb")
    statistic_card_product = relationship("WBStatisticCardProduct", back_populates="card_product")
    statistic_advert = relationship("WBStatisticAdvert", back_populates="card_product")


class WBStatisticCardProduct(Base):
    """Модель таблицы wb_statistic_card_product."""
    __tablename__ = 'wb_statistic_card_product'

    id = Column(Integer, Identity(), primary_key=True)
    sku = Column(String(length=255), ForeignKey('wb_card_product.sku'), nullable=False)
    date = Column(Date, nullable=False)
    open_card_count = Column(Integer, nullable=False)
    add_to_cart_count = Column(Integer, nullable=False)
    orders_count = Column(Integer, nullable=False)
    add_to_cart_percent = Column(Numeric(precision=12, scale=2), nullable=False)
    cart_to_order_percent = Column(Numeric(precision=12, scale=2), nullable=False)
    price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)
    discount_price = Column(Numeric(precision=12, scale=2), default=None, nullable=True)

    card_product = relationship("WBCardProduct", back_populates="statistic_card_product")


class WBStatisticAdvert(Base):
    """Модель таблицы wb_statistic_advert."""
    __tablename__ = 'wb_statistic_advert'

    id = Column(Integer, Identity(), primary_key=True)
    sku = Column(String(length=255), ForeignKey('wb_card_product.sku'), nullable=False)
    advert_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    views = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    ctr = Column(Numeric(precision=12, scale=2), nullable=False)
    cpc = Column(Numeric(precision=12, scale=2), nullable=False)
    atbs = Column(Integer, nullable=False)
    orders_count = Column(Integer, nullable=False)
    shks = Column(Integer, nullable=False)
    sum_price = Column(Numeric(precision=12, scale=2), nullable=False)
    sum_cost = Column(Numeric(precision=12, scale=2), nullable=False)
    appType = Column(Unicode, default=None, nullable=True)

    card_product = relationship("WBCardProduct", back_populates="statistic_advert")


class WBTypeAdvert(Base):
    """Модель таблицы wb_type_advert."""
    __tablename__ = 'wb_type_advert'

    id_type = Column(Integer, primary_key=True)
    type = Column(Unicode, default=None, nullable=True)

    advert_type_id = relationship("WBAdverts", back_populates="advert_type")


class WBStatusAdvert(Base):
    """Модель таблицы wb_status_advert."""
    __tablename__ = 'wb_status_advert'

    id_status = Column(Integer, primary_key=True)
    status = Column(Unicode, default=None, nullable=True)

    advert_status_id = relationship("WBAdverts", back_populates="advert_status")


class WBAdverts(Base):
    """Модель таблицы wb_adverts_table."""
    __tablename__ = 'wb_adverts_table'

    id_advert = Column(Integer, primary_key=True)
    client_id = Column(String(length=255), ForeignKey('clients.client_id'), nullable=False)
    id_type = Column(Integer, ForeignKey('wb_type_advert.id_type'), nullable=False)
    id_status = Column(Integer, ForeignKey('wb_status_advert.id_status'), nullable=False)
    name_advert = Column(Unicode, default=None, nullable=True)
    create_time = Column(Date)
    change_time = Column(Date)
    start_time = Column(Date)
    end_time = Column(Date)

    advert_type = relationship("WBTypeAdvert", back_populates="advert_type_id", cascade="all, save-update, merge")
    advert_status = relationship("WBStatusAdvert", back_populates="advert_status_id", cascade="all, save-update, merge")
    client = relationship("Client", back_populates="adverts_wb")


class DateList(Base):
    """Модель таблицы date."""
    __tablename__ = 'date'

    date = Column(Date, primary_key=True)
