from .base import BaseResponse


class NmReportDownloadsResponse(BaseResponse):
    """Создать отчёт по воронке продаж."""
    data: str
