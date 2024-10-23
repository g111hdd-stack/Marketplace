from typing import Optional

from .base import BaseResponse
from ..entities import PostingFBSGet


class PostingFBSGetResponse(BaseResponse):
    """Информация об отправлении."""
    result: Optional[PostingFBSGet] = []
