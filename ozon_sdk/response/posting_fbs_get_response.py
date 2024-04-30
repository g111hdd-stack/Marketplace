from .base import BaseResponse
from ..entities import PostingFBSGet


class PostingFBSGetResponse(BaseResponse):
    """Информация об отправлении."""
    result: PostingFBSGet
