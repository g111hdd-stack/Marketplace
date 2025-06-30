from pydantic import Field
from typing import Optional

from .base import BaseRequest


class CardsListQueryRequest(BaseRequest):
    """Получить информацию о карточках товаров."""
    locale: Optional[str] = 'ru'


class CardsListSettingsSortBodyRequest(BaseRequest):
    """Параметр сортировки."""
    ascending: Optional[bool] = False


class CardsListSettingsFilterBodyRequest(BaseRequest):
    """Параметры фильтрации."""
    withPhoto: Optional[int] = -1
    textSearch: Optional[str] = None
    tagIDs: Optional[list[int]] = []
    allowedCategoriesOnly: Optional[bool] = False
    objectIDs: Optional[list[int]] = []
    brands: Optional[list[str]] = []
    imtID: Optional[int] = None


class CardsListSettingsCursorBodyRequest(BaseRequest):
    """Курсор."""
    limit: Optional[int] = 100
    updatedAt: Optional[str] = None
    nmID: Optional[int] = None


class CardsListSettingsBodyRequest(BaseRequest):
    """Настройки."""
    sort: CardsListSettingsSortBodyRequest
    filter_field: CardsListSettingsFilterBodyRequest = Field(default=None, alias='filter')
    cursor: CardsListSettingsCursorBodyRequest


class CardsListBodyRequest(BaseRequest):
    """Получить информацию о карточках товаров."""
    settings: CardsListSettingsBodyRequest
