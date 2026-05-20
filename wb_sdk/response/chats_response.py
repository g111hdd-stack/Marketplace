from typing import Optional

from .base import BaseResponse
from ..entities import Chats


class ChatsResponse(BaseResponse):
    """Возвращает информацию о чатах с покупателем."""
    result: list[Chats]
    errors: Optional[list[str]]
