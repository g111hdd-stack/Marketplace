from .base import BaseRequest


class AnalyticsAntifraudDetailsRequest(BaseRequest):
    """Запрос отчётапо удержаниям за самовыкупы."""
    date: str
