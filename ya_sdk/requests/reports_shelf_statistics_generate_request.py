from pydantic import Field

from .base import BaseRequest


class ReportsShelfStatisticsGenerateQueryRequest(BaseRequest):
    """Отчет по полкам. Query."""
    format_field: str = Field(default='FILE', alias='format')


class ReportsShelfStatisticsGenerateBodyRequest(BaseRequest):
    """Отчет по полкам. Body."""
    attributionType: str
    businessId: int
    dateFrom: str
    dateTo: str
