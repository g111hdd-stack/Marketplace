from .base import BaseResponse
from ..entities import GetWarehouseStocksDTO


class CampaignsOffersStocksResponse(BaseResponse):
    """Информация о остатках на складах."""
    result: GetWarehouseStocksDTO
    status: str
