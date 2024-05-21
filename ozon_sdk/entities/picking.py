from datetime import datetime

from .base import BaseEntity


class Picking(BaseEntity):
    """Информация о доставке."""
    amount: float
    moment: datetime
    tag: str
