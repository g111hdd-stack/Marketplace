from typing import Optional

from .base import BaseEntity


class ListGoodSize(BaseEntity):
    """Размер."""
    sizeID: int = None
    price: float = None
    discountedPrice: float = None
    techSizeName: str = None


class ListGood(BaseEntity):
    """Информация о товаре."""
    nmID: int = None
    vendorCode: str = None
    sizes: Optional[list[ListGoodSize]] = []
    currencyIsoCode4217: str = None
    discount: int = None
    editableSizePrice: bool = None


class ListGoodsFilter(BaseEntity):
    """Информация о товарах."""
    listGoods: Optional[list[ListGood]] = []
