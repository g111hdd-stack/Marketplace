from typing import Optional

from .base import BaseResponse
from ..entities import SupplierSales


class SupplierSalesResponse(BaseResponse):
    """Продажи."""
    result: Optional[list[SupplierSales]] = []
