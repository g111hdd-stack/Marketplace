from typing import Optional
from datetime import datetime
from pydantic import Field

from .base import BaseEntity
from .price_indexes import PriceIndexes


class ProductInfoListItemDiscountedStocks(BaseEntity):
    """Остатки уценённого товара на складе Ozon."""
    coming: int = None
    present: int = None
    reserved: int = None


class ItemErrorOptionalDescriptionElements(BaseEntity):
    """Дополнительные поля для описания ошибки."""
    pass


class ItemError(BaseEntity):
    """Ошибки при загрузке товаров."""
    code: str = None
    state: str = None
    level: str = None
    description: str = None
    field: str = None
    attribute_id: int = None
    attribute_name: str = None
    optional_description_elements: Optional[ItemErrorOptionalDescriptionElements] = None


class ProductInfoListItemStatus(BaseEntity):
    """Описание состояния товара."""
    state: str = None
    state_failed: str = None
    moderate_status: str = None
    decline_reasons: Optional[list[str]] = []
    validation_state: str = None
    state_name: str = None
    state_description: str = None
    is_failed: bool = None
    is_created: bool = None
    state_tooltip: str = None
    item_errors: Optional[list[ItemError]] = []
    state_updated_at: datetime = None


class ProductInfoListSource(BaseEntity):
    """Информация об источниках схожих предложений."""
    is_enabled: bool = None
    sku: int = None
    source: str = None


class ProductInfoListItemStocks(BaseEntity):
    """Информация об остатках товара."""
    coming: int = None
    present: int = None
    reserved: int = None


class VisibilityDetailsReasons(BaseEntity):
    """Причина, почему товар скрыт."""
    pass


class ProductInfoListVisibilityDetails(BaseEntity):
    """Настройки видимости товара."""
    active_product: bool = None
    has_price: bool = None
    has_stock: bool = None
    reasons: Optional[VisibilityDetailsReasons] = None


class ProductInfoListItem(BaseEntity):
    """Информация о товаре."""
    is_archived: bool = None
    is_autoarchived: bool = None
    barcode: str = None
    barcodes: Optional[list[str]] = []
    buybox_price: str = None
    description_category_id: int = None
    type_id: int = None
    color_image: str = None
    created_at: datetime = None
    sku: int = None
    id_field: int = Field(default=None, alias='id')
    images: Optional[list[str]] = []
    primary_image: str = None
    images360: Optional[list[str]] = None
    has_discounted_item: bool = None
    is_discounted: bool = None
    category_id: int = None
    discounted_stocks: Optional[ProductInfoListItemDiscountedStocks] = None
    is_kgt: bool = None
    currency_code: str = None
    marketing_price: str = None
    min_ozon_price: str = None
    min_price: str = None
    name: str = None
    offer_id: str = None
    old_price: str = None
    price: str = None
    price_index: str = None
    price_indexes: Optional[PriceIndexes] = None
    recommended_price: str = None
    status: Optional[ProductInfoListItemStatus] = None
    sources: Optional[list[ProductInfoListSource]] = []
    stocks: Optional[ProductInfoListItemStocks] = None
    updated_at: datetime = None
    vat: str = None
    visibility_details: Optional[ProductInfoListVisibilityDetails] = None
    visible: bool = None


class ProductInfoList(BaseEntity):
    """Результаты запроса."""
    items: Optional[list[ProductInfoListItem]] = []
