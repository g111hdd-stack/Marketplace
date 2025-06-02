from typing import Optional

from .base import BaseResponse
from ..entities import GetOfferMappingsResultDTO


class BusinessesOfferMappingsResponse(BaseResponse):
    """Информация о товарах в каталоге."""
    status: str = None
    result: Optional[GetOfferMappingsResultDTO] = None
