from .base import BaseEntity


class Error(BaseEntity):
    """Дополнительные ошибки."""
    field: str = None
    description: str = None
