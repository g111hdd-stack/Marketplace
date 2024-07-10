from .base import BaseEntity


class ReportInfoDTO(BaseEntity):
    """Статус генерации и ссылка на готовый отчет."""
    status: str = None
    subStatus: str = None
    generationRequestedAt: str = None
    generationFinishedAt: str = None
    file: str = None
    estimatedGenerationTime: int = None
