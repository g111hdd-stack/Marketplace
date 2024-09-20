from typing import Optional

from .base import BaseResponse
from ..entities import WarehouseRemainsTasksStatus


class WarehouseRemainsTasksStatusResponse(BaseResponse):
    """Статус отчёт по остаткам на складах."""
    data: Optional[WarehouseRemainsTasksStatus] = None
