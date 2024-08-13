from .base import BaseResponse
from ..entities import PaidStorageStatus


class PaidStorageStatusResponse(BaseResponse):
    """Статус отчёта по хранению."""
    data: PaidStorageStatus
