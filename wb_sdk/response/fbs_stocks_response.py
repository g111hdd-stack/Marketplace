from .base import BaseResponse
from ..entities import FBSStocks


class FBSStocksResponse(BaseResponse):
    """Возвращает информацию об остатках на складе FBS."""
    stocks: list[FBSStocks] = []
