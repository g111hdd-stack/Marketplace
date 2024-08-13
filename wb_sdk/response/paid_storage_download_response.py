from .base import BaseResponse
from ..entities import PaidStorageReport


class PaidStorageDownloadResponse(BaseResponse):
    """Получить отчёт по хранению."""
    result: list[PaidStorageReport] = []
