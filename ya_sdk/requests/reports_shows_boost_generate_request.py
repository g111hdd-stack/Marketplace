from pydantic import Field

from .base import BaseRequest


class ReportsShowsBoostGenerateQueryRequest(BaseRequest):
    """Отчет по бусту показов. Query."""
    format_field: str = Field(default='FILE', alias='format')


class ReportsShowsBoostGenerateBodyRequest(BaseRequest):
    """Отчет по бусту показов. Body."""
    attributionType: str
    businessId: int
    dateFrom: str
    dateTo: str
