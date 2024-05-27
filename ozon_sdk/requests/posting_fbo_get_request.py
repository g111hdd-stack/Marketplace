from typing import Optional

from pydantic import Field

from .base import BaseRequest


class PostingFBOGetWith(BaseRequest):
    """Дополнительные поля, которые нужно добавить в ответ."""
    analytics_data: Optional[bool] = False
    financial_data: Optional[bool] = False


class PostingFBOGetRequest(BaseRequest):
    """Возвращает информацию об отправлении по его идентификатору."""
    posting_number: str
    translit: Optional[bool] = False
    with_field: PostingFBOGetWith = Field(default=PostingFBOGetWith, serialization_alias='with')
