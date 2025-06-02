from typing import Optional

from .base import BaseRequest


class BusinessesOfferMappingsQueryRequest(BaseRequest):
    """Информация о товарах в каталоге. Query."""
    language: Optional[str]
    page_token: Optional[str]
    limit: int = 20


class BusinessesOfferMappingsBodyRequest(BaseRequest):
    """Информация о товарах в каталоге. Body."""
    archived: Optional[bool]
    cardStatuses: Optional[list[str]] = []
    categoryIds: Optional[list[int]] = []
    offerIds: Optional[list[str]] = []
    tags: Optional[list[str]] = []
    vendorNames: Optional[list[str]] = []
