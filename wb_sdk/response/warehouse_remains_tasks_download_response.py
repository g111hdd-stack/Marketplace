from typing import Optional

from .base import BaseResponse
from ..entities import WarehouseRemainsTasksDownload


class WarehouseRemainsTasksDownloadResponse(BaseResponse):
    """Получить отчёт по остаткам на складах."""
    result: Optional[list[WarehouseRemainsTasksDownload]] = None
