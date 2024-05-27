from typing import Optional

from pydantic import Field

from .base import BaseRequest


class PostingFBSGetWith(BaseRequest):
    """Дополнительные поля, которые нужно добавить в ответ."""
    analytics_data: Optional[bool] = False
    barcodes: Optional[bool] = False
    financial_data: Optional[bool] = False
    product_exemplars: Optional[bool] = False
    related_postings: Optional[bool] = False
    translit: Optional[bool] = False


class PostingFBSGetRequest(BaseRequest):
    """Возвращает информацию об отправлении по его идентификатору."""
    posting_number: str
    with_field: PostingFBSGetWith = Field(default=PostingFBSGetWith, serialization_alias='with')
