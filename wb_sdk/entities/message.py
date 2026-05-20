from typing import Optional

from .base import BaseEntity


class Message(BaseEntity):
    """Сообщение."""
    addTime: Optional[int] = None
    chatID: str = None
    sign: str = None
