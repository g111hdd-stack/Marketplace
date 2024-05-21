from typing import Optional

from .base import BaseEntity


class ProductListItem(BaseEntity):
    """Товар."""
    offer_id: str = None
    product_id: int = None


class ProductList(BaseEntity):
    """Результат."""
    items: Optional[list[ProductListItem]] = []
    last_id: str = None
    total: int = None
