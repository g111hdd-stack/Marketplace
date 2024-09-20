from .base import BaseResponse


class NmReportDownloadsFileResponse(BaseResponse):
    """Получить отчёт по воронке продаж."""
    file: bytes
