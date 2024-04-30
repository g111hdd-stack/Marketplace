from datetime import datetime
from typing import Optional

from .base import BaseEntity


class FinanceTransactionListOperationItem(BaseEntity):
    """Информация о товаре."""
    name: str = None
    sku: int = None


class FinanceTransactionListOperationPosting(BaseEntity):
    """Информация об отправлении."""
    delivery_schema: str = None
    order_date: str = None
    posting_number: str = None
    warehouse_id: int = None


class FinanceTransactionListOperationService(BaseEntity):
    """Дополнительные услуги."""
    name: str = None
    price: float = None


class FinanceTransactionListOperation(BaseEntity):
    """Информация об операции."""
    accruals_for_sale: float = None
    amount: float = None
    delivery_charge: float = None
    items: list[FinanceTransactionListOperationItem] = []
    operation_date: datetime = None
    operation_id: int = None
    operation_type: str = None
    operation_type_name: str = None
    posting: Optional[FinanceTransactionListOperationPosting] = None
    return_delivery_charge: float = None
    sale_commission: float = None
    services: list[FinanceTransactionListOperationService] = None
    type: str = None


class FinanceTransactionList(BaseEntity):
    """Результаты запроса."""
    operations: list[FinanceTransactionListOperation] = []
    page_count: int = None
    row_count: int = None
