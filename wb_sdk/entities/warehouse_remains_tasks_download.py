from typing import Optional

from .base import BaseEntity


class WarehouseRemainsTasksDownloadWarehouse(BaseEntity):
    """Склады."""
    warehouseName: str
    quantity: int


class WarehouseRemainsTasksDownload(BaseEntity):
    """Получить отчёт по остаткам на складах."""
    brand: Optional[str] = None
    subjectName: Optional[str] = None
    vendorCode: Optional[str] = None
    nmId: Optional[int] = None
    barcode: Optional[str] = None
    techSize: Optional[str] = None
    volume: Optional[float] = None
    inWayToClient: int
    inWayFromClient: int
    quantityWarehousesFull: int
    warehouses: Optional[list[WarehouseRemainsTasksDownloadWarehouse]] = []
