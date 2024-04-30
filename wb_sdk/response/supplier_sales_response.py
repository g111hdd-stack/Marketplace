from .base import BaseResponse
from ..entities import SupplierSales


class SupplierSalesResponse(BaseResponse):
    """Продажи"""
    result: list[SupplierSales] = []
