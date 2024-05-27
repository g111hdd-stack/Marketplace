from .base import BaseResponse


class ClientStatisticsJSONResponse(BaseResponse):
    """Статистика по кампании."""
    UUID: str = None
    vendor: bool = None

