from typing import Optional

from .base import BaseRequest
from pydantic import Field


class FinanceTransactionListDate(BaseRequest):
    """Фильтр по дате."""
    from_field: str = Field(serialization_alias='from')
    to: str


class FinanceTransactionListFilter(BaseRequest):
    """Фильтр."""
    date: FinanceTransactionListDate
    operation_type: Optional[list[str]] = []
    posting_number: Optional[str] = None
    transaction_type: Optional[str] = 'ALL'


class FinanceTransactionListRequest(BaseRequest):
    """Возвращает подробную информацию по всем начислениям."""
    filter: FinanceTransactionListFilter
    page: int = 1
    page_size: int = 1000
