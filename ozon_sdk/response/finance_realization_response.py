from typing import Optional

from .base import BaseResponse
from ..entities import FinanceRealization


class FinanceRealizationResponse(BaseResponse):
    """Отчёт о реализации товаров."""
    result: Optional[FinanceRealization] = None
