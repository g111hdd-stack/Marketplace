from pydantic import Field

from .base import BaseRequest


class ReportsBoostConsolidatedGenerateQueryRequest(BaseRequest):
    """Отчет по бусту продаж. Query."""
    format_field: str = Field(default='FILE', alias='format')


class ReportsBoostConsolidatedGenerateBodyRequest(BaseRequest):
    """Отчет по бусту продаж. Body."""
    businessId: int
    dateFrom: str
    dateTo: str
