from typing import Optional

from .base import BaseRequest


class MessageRequest(BaseRequest):
    replySign: str
    message: str
    file: Optional[list[str]] = None
