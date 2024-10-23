from typing import Optional

from .base import BaseResponse
from ..entities import PostingFBSList


class PostingFBSListResponse(BaseResponse):
    """Информация об отправлениях."""
    result: Optional[PostingFBSList] = None
