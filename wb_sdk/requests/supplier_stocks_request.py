from .base import BaseRequest


class SupplierStocksRequest(BaseRequest):
    """Запрос по остаткам на складах."""
    dateFrom: str
