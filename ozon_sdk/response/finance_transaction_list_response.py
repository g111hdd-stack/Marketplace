from typing import Optional

from .base import BaseResponse
from ..entities import FinanceTransactionList


class FinanceTransactionListResponse(BaseResponse):
    """Результаты запроса."""
    result: Optional[FinanceTransactionList] = None
