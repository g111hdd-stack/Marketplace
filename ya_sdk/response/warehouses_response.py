from .base import BaseResponse
from ..entities import FulfillmentWarehousesDTO


class WarehousesResponse(BaseResponse):
    """Информация о складах."""
    result: FulfillmentWarehousesDTO
    status: str
