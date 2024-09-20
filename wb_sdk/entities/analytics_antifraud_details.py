from .base import BaseEntity


class AnalyticsAntifraudDetails(BaseEntity):
    """Отчёт о удержаниям за самовыкупы."""
    nmID: int = None
    sum: int = None
    currency: str = None
    dateFrom: str = None
    dateTo: str = None
