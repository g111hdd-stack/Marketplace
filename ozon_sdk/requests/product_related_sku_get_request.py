from .base import BaseRequest


class ProductRelatedSkuGetRequest(BaseRequest):
    """Метод для получения единого SKU по старым идентификаторам SKU FBS и SKU FBO."""
    sku: list[str]
