from typing import Optional

from .base import BaseResponse
from ..entities import WarehouseRemains


class WarehouseRemainsResponse(BaseResponse):
    """Создать отчёт по остаткам на складах."""
    data: Optional[WarehouseRemains]
