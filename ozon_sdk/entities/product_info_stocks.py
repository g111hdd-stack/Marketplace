from typing import Optional

from .base import BaseEntity


class ProductInfoStocksItemStock(BaseEntity):
    present: int = None
    reserved: int = None
    type: str = None


class ProductInfoStocksItem(BaseEntity):
    """Товар."""
    offer_id: str = None
    product_id: int = None
    stocks: Optional[list[ProductInfoStocksItemStock]] = []


class ProductInfoStocks(BaseEntity):
    """Результат."""
    items: Optional[list[ProductInfoStocksItem]] = []
    last_id: str = None
    total: int = None
