from .base import BaseRequest


class FBSStocksRequest(BaseRequest):
    """Получить информацию об остатках FBS."""
    skus: list[str]
