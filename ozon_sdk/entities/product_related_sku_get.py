from datetime import datetime
from typing import Optional

from .base import BaseEntity


class ProductRelatedSkuGetError(BaseEntity):
    """Ошибка."""
    code: str = None
    sku: int = None
    message: str = None


class ProductRelatedSkuGet(BaseEntity):
    """Результат."""
    availability: str = None
    deleted_at: Optional[datetime] = None
    delivery_schema: str = None
    product_id: int = None
    sku: int = None
