from datetime import datetime

from .base import BaseEntity


class Picking(BaseEntity):
    """
        Информация о доставке. \n
        Всегда возвращает null.
    """
    amount: float
    moment: datetime
    tag: str
