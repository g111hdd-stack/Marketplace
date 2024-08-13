from .base import BaseEntity


class PaidStorageReport(BaseEntity):
    date: str = None
    logWarehouseCoef: float = None
    officeId: int = None
    warehouse: str = None
    warehouseCoef: float = None
    giId: int = None
    chrtId: int = None
    size: str = None
    barcode: str = None
    subject: str = None
    brand: str = None
    vendorCode: str = None
    nmId: int = None
    volume: float = None
    calcType: str = None
    warehousePrice: float = None
    barcodesCount: int = None
    palletPlaceCode: int = None
    palletCount: float = None
    originalDate: str = None
    loyaltyDiscount: float = None
    tariffFixDate: str = None
    tariffLowerDate: str = None
