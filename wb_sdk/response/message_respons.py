from typing import Optional

from .base import BaseResponse
from ..entities import Message


class MessageResponse(BaseResponse):
    """Возвращает информацию о доставки сообщения в чат."""
    errors: Optional[list[str]]
    result: Optional[Message]
