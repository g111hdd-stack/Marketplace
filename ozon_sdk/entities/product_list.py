from typing import Optional

from .base import BaseEntity


class ProductListItemQuants(BaseEntity):
    quant_code: str
    quant_size: int


class ProductListItem(BaseEntity):
    """Товар."""
    archived: bool = None
    has_fbo_stocks: bool = None
    has_fbs_stocks: bool = None
    is_discounted: bool = None
    offer_id: str = None
    product_id: int = None
    quants: Optional[ProductListItemQuants] = None


class ProductList(BaseEntity):
    """Результат."""
    items: Optional[list[ProductListItem]] = []
    last_id: str = None
    total: int = None
