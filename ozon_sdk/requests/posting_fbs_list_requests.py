from typing import Optional

from pydantic import Field

from .base import BaseRequest


class PostingFBSListFilterLastChangedStatusDate(BaseRequest):
    """Период, в который последний раз изменялся статус у отправлений."""
    from_field: Optional[str] = Field(default=None, serialization_alias='from')
    to: Optional[str]


class PostingFBSListFilter(BaseRequest):
    """Фильтр для поиска отправлений."""
    delivery_method_id: Optional[list[int]] = []
    order_id: Optional[int] = None
    provider_id: Optional[list[int]] = []
    since: str
    status: Optional[str] = ""
    warehouse_id: Optional[list[int]] = []
    to: str
    last_changed_status_date: Optional[PostingFBSListFilterLastChangedStatusDate] = None


class PostingFBSListWith(BaseRequest):
    """Дополнительные поля, которые нужно добавить в ответ."""
    analytics_data: Optional[bool] = False
    barcodes: Optional[bool] = False
    financial_data: Optional[bool] = False
    translit: Optional[bool] = False


class PostingFBSListRequest(BaseRequest):
    """Возвращает информацию об отправленях."""
    order_by: Optional[str] = Field(default=PostingFBSListWith, serialization_alias='dir')
    filter: PostingFBSListFilter
    limit: Optional[int] = 1000
    offset: Optional[int] = 0
    with_field: PostingFBSListWith = Field(default=PostingFBSListWith, serialization_alias='with')
