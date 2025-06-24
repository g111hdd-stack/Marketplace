from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, MetaData, Integer, Identity
from sqlalchemy import UniqueConstraint, Numeric, ForeignKey, DateTime, Boolean

metadata = MetaData()
Base = declarative_base(metadata=metadata)

MOSCOW_TZ = timezone(timedelta(hours=3))


def round_to_5_minutes_moscow():
    now_msk = datetime.now(MOSCOW_TZ).replace(tzinfo=None)
    floored_minutes = (now_msk.minute // 5) * 5
    rounded = now_msk.replace(minute=floored_minutes, second=0, microsecond=0)
    return rounded


class Client(Base):
    """Модель таблицы clients."""
    __tablename__ = 'clients'

    client_id = Column(String(length=20), primary_key=True)
    name_company = Column(String(length=60), nullable=False)
    entrepreneur = Column(String(length=60), nullable=False)

    products = relationship("Product", back_populates="client")


class Product(Base):
    """Модель таблицы products."""
    __tablename__ = 'products'

    sku = Column(String(length=20), primary_key=True)
    client_id = Column(String(length=20), ForeignKey('clients.client_id'), nullable=False)
    vendor_code = Column(String(length=60), nullable=False)

    client = relationship("Client", back_populates="products")
    queries = relationship("Query", back_populates="product")


class Query(Base):
    """Модель таблицы queries."""
    __tablename__ = 'queries'

    id_query = Column(Integer, Identity(), primary_key=True)
    sku = Column(String(length=20), ForeignKey('products.sku'), nullable=False)
    query = Column(String(length=300), nullable=False)
    is_track = Column(Boolean, default=True, nullable=False)

    product = relationship("Product", back_populates="queries")
    ratings = relationship("Rating", back_populates="query")


class Rating(Base):
    """Модель таблицы ratings."""
    __tablename__ = 'ratings'

    id = Column(Integer, Identity(), primary_key=True)
    query_id = Column(Integer, ForeignKey('queries.id_query'), nullable=False)
    collected_at = Column(DateTime(timezone=False), nullable=False, default=round_to_5_minutes_moscow)
    cpm = Column(Numeric(precision=12, scale=2), nullable=True)
    promo_position = Column(Integer, nullable=True)
    position = Column(Integer, nullable=True)
    advert_id = Column(String(length=20), nullable=True)

    query = relationship("Query", back_populates="ratings")

    __table_args__ = (
        UniqueConstraint('query_id', 'collected_at', name='ratings_unique'),
    )
