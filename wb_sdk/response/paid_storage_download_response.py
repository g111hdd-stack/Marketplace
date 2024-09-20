from typing import Optional

from .base import BaseResponse
from ..entities import PaidStorageReport


class PaidStorageDownloadResponse(BaseResponse):
    """Получить отчёт по хранению."""
    result: Optional[list[PaidStorageReport]] = []
