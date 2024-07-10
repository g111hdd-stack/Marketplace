from typing import Optional
from pydantic import Field

from .base import BaseRequest


class ReportsUnitedMarketplaceServicesGenerateQueryRequest(BaseRequest):
    """Отчет по стоимости услуг. Query."""
    format_field: str = Field(default='FILE', alias='format')
    language: Optional[str] = 'RU'


class ReportsUnitedMarketplaceServicesGenerateBodyRequest(BaseRequest):
    """Отчет по стоимости услуг. Body."""
    businessId: Optional[int]
    dateTimeFrom: Optional[str]
    dateTimeTo: Optional[str]
    dateFrom: Optional[str]
    dateTo: Optional[str]
    yearFrom: Optional[int]
    monthFrom: Optional[int]
    yearTo: Optional[int]
    monthTo: Optional[int]
    placementPrograms: Optional[list[str]]
    inns: Optional[list[str]]
    campaignIds: Optional[list[int]]
