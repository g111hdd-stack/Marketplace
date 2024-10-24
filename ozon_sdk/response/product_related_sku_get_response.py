from typing import Optional

from .base import BaseResponse
from ..entities import ProductRelatedSkuGet, ProductRelatedSkuGetError


class ProductRelatedSkuGetResponse(BaseResponse):
    """Получение единого SKU по старым идентификаторам SKU FBS и SKU FBO. """
    items: Optional[list[ProductRelatedSkuGet]] = []
    errors: Optional[list[ProductRelatedSkuGetError]] = []
