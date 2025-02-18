from typing import Optional
from datetime import datetime
from pydantic import Field

from .base import BaseEntity
from .price_indexes import PriceIndexes


class ProductInfoListCommission(BaseEntity):
    delivery_amount: float = None
    percent: float = None
    return_amount: float = None
    sale_schema: str = None
    value: float = None


class ItemErrorTextsParam(BaseEntity):
    name: str = None
    value: str = None


class ItemErrorTexts(BaseEntity):
    attribute_name: str = None
    description: str = None
    hint_code: str = None
    message: str = None
    params: Optional[list[ItemErrorTextsParam]] = []
    short_description: str = None


class ItemError(BaseEntity):
    """Ошибки при загрузке товаров."""
    attribute_id: int = None
    code: str = None
    field: str = None
    level: str = None
    state: str = None
    texts: Optional[ItemErrorTexts] = None


class ProductInfoListModelInfo(BaseEntity):
    count: int = None
    model_id: int = None

    class Config:
        protected_namespaces = ()


class ProductInfoListItemStatus(BaseEntity):
    """Описание состояния товара."""
    is_created: bool = None
    moderate_status: str = None
    status: str = None
    status_description: str = None
    status_failed: str = None
    state_name: str = None
    state_tooltip: str = None
    state_updated_at: datetime = None
    validation_state: str = None


class ProductInfoListSource(BaseEntity):
    """Информация об источниках схожих предложений."""
    created_at: datetime = None
    quant_code: str = None
    shipment_type: str = None
    sku: int = None
    source: str = None


class ProductInfoListItemStock(BaseEntity):
    """Информация об остатках товара."""
    sku: int = None
    present: int = None
    reserved: int = None
    source: str = None


class ProductInfoListItemStocks(BaseEntity):
    """Информация об остатках товара."""
    has_stock: bool = None
    stocks: Optional[list[ProductInfoListItemStock]] = []


class ProductInfoListVisibilityDetails(BaseEntity):
    """Настройки видимости товара."""
    has_price: bool = None
    has_stock: bool = None


class ProductInfoListItem(BaseEntity):
    """Информация о товаре."""
    barcodes: Optional[list[str]] = []
    color_image: Optional[list[str]] = []
    commissions: Optional[list[ProductInfoListCommission]] = []
    created_at: datetime = None
    currency_code: str = None
    description_category_id: int = None
    discounted_fbo_stocks: int = None
    errors: Optional[list[ItemError]] = []
    has_discounted_fbo_item: bool = None
    id_field: int = Field(default=None, alias='id')
    images: Optional[list[str]] = []
    images360: Optional[list[str]] = None
    is_archived: bool = None
    is_autoarchived: bool = None
    is_discounted: bool = None
    is_kgt: bool = None
    is_prepayment_allowed: bool = None
    is_super: bool = None
    marketing_price: str = None
    min_price: str = None
    model_info: Optional[ProductInfoListModelInfo] = None
    name: str = None
    offer_id: str = None
    old_price: str = None
    price: str = None
    price_indexes: Optional[PriceIndexes] = None
    primary_image: Optional[list[str]] = []
    sources: Optional[list[ProductInfoListSource]] = []
    statuses: Optional[ProductInfoListItemStatus] = None
    stocks: Optional[ProductInfoListItemStocks] = None
    type_id: int = None
    updated_at: datetime = None
    vat: str = None
    visibility_details: Optional[ProductInfoListVisibilityDetails] = None
    volume_weight: float = None

    class Config:
        protected_namespaces = ()
