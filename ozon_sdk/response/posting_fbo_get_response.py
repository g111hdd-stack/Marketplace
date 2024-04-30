from .base import BaseResponse
from ..entities import PostingFBOGet


class PostingFBOGetResponse(BaseResponse):
    """Информация об отправлении."""
    result: PostingFBOGet
