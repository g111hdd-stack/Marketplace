from .base import BaseEntity


class GenerateReportDTO(BaseEntity):
    """Отчет по стоимости услуг."""
    reportId: str = None
    estimatedGenerationTime: int = None
