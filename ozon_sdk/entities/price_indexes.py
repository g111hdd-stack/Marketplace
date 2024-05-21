from typing import Optional

from .base import BaseEntity


class PriceIndexesData(BaseEntity):
    """Цена товара."""
    minimal_price: str = None
    minimal_price_currency: str = None
    price_index_value: float = None


class PriceIndexes(BaseEntity):
    """Ценовые индексы товара."""
    external_index_data: Optional[PriceIndexesData] = None
    ozon_index_data: Optional[PriceIndexesData] = None
    price_index: str = None
    self_marketplaces_index_data: Optional[PriceIndexesData] = None
