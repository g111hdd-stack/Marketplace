from datetime import datetime

from .base import BaseEntity


class SupplierOrders(BaseEntity):
    """Заказы."""
    date: datetime = None
    lastChangeDate: datetime = None
    warehouseName: str = None
    warehouseType: str = None
    countryName: str = None
    oblastOkrugName: str = None
    regionName: str = None
    supplierArticle: str = None
    nmId: int = None
    barcode: str = None
    category: str = None
    subject: str = None
    brand: str = None
    techSize: str = None
    incomeID: int = None
    isSupply: bool = None
    isRealization: bool = None
    totalPrice: float = None
    discountPercent: int = None
    spp: float = None
    finishedPrice: float = None
    priceWithDisc: float = None
    isCancel: bool = None
    cancelDate: datetime = None
    sticker: str = None
    gNumber: str = None
    srid: str = None
