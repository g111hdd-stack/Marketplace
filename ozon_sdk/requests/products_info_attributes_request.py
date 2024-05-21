from typing import Optional

from .base import BaseRequest


class ProductsInfoAttributesFilter(BaseRequest):
    offer_id: Optional[list[str]] = []
    product_id: Optional[list[str]] = []
    visibility: Optional[str] = None


class ProductsInfoAttributesRequest(BaseRequest):
    filter: ProductsInfoAttributesFilter
    last_id: Optional[str] = None
    limit: int = 100
    sort_by: Optional[str] = None
    sort_dir: Optional[str] = None
