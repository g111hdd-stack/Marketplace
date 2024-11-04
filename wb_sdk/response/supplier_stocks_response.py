from typing import Optional

from .base import BaseResponse
from ..entities import SupplierStocks


class SupplierStocksResponse(BaseResponse):
    """Создать отчёт по остаткам на складах."""
    result: Optional[list[SupplierStocks]] = []
