from .base import BaseEntity


class GenerateReportDTO(BaseEntity):
    """Отчет."""
    reportId: str = None
    estimatedGenerationTime: int = None
