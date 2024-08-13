from .base import BaseResponse
from ..entities import PaidStorage


class PaidStorageResponse(BaseResponse):
    """Создать отчёт по хранению."""
    data: PaidStorage
