from .base import BaseRequest


class PaidStorageRequest(BaseRequest):
    dateFrom: str
    dateTo: str
