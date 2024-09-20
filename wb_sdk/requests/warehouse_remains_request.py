from typing import Optional

from .base import BaseRequest


class WarehouseRemainsRequest(BaseRequest):
    """Создать отчёт по остаткам на складах."""
    locale: Optional[str] = "ru"
    groupByBrand: Optional[str] = 'false'
    groupBySubject: Optional[str] = 'false'
    groupBySa: Optional[str] = 'false'
    groupByNm: Optional[str] = 'false'
    groupByBarcode: Optional[str] = 'false'
    groupBySize: Optional[str] = 'false'
    filterPics: Optional[int] = 0
    filterVolume: Optional[int] = 0
