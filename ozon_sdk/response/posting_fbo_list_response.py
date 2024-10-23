from .base import BaseResponse
from ..entities import PostingFBOList


class PostingFBOListResponse(BaseResponse):
    """Информация об отправлениях."""
    result: list[PostingFBOList] = []
