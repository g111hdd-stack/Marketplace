from .base import BaseEntity


class FBSStocks(BaseEntity):
    """Остатки на складе FBS."""
    sku: str = None
    amount: int = None

