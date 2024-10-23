from typing import Optional

from pydantic import Field

from .base import BaseRequest


class PostingFBOListFilter(BaseRequest):
    """Фильтр для поиска отправлений."""
    since: str
    status: Optional[str] = ""
    to: str


class PostingFBOListWith(BaseRequest):
    """Дополнительные поля, которые нужно добавить в ответ."""
    analytics_data: Optional[bool] = False
    financial_data: Optional[bool] = False


class PostingFBOListRequest(BaseRequest):
    """Возвращает информацию об отправленях."""
    order_by: Optional[str] = Field(default=PostingFBOListWith, serialization_alias='dir')
    filter: PostingFBOListFilter
    limit: Optional[int] = 1000
    offset: Optional[int] = 0
    translit: Optional[bool] = False
    with_field: PostingFBOListWith = Field(default=PostingFBOListWith, serialization_alias='with')
