from typing import Optional

from .base import BaseEntity


class ProductInfoStocksItemStock(BaseEntity):
    present: int = None
    reserved: int = None
    shipment_type: str = None
    sku: int = None
    type: str = None


class ProductInfoStocksItem(BaseEntity):
    """Товар."""
    offer_id: str = None
    product_id: int = None
    stocks: Optional[list[ProductInfoStocksItemStock]] = []
