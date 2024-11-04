from datetime import datetime

from .base import BaseEntity


class SupplierStocks(BaseEntity):
    """Остатки на складах."""
    lastChangeDate: datetime = None
    warehouseName: str = None
    supplierArticle: str = None
    nmId: int = None
    barcode: str = None
    quantity: int = None
    inWayToClient: int = None
    inWayFromClient: int = None
    quantityFull: int = None
    category: str = None
    subject: str = None
    brand: str = None
    techSize: str = None
    Price: float = None
    Discount: float = None
    isSupply: bool = None
    isRealization: bool = None
    SCCode: str = None
