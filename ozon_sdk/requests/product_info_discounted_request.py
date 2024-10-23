from .base import BaseRequest


class ProductInfoDiscountedRequest(BaseRequest):
    """Получить информацию о состоянии и дефектах уценённого товара по его SKU."""
    discounted_skus: list[str]

