from pydantic import Field
from typing import Optional

from .base import BaseEntity


class PromotionAdvertsParaminterval(BaseEntity):
    """Интервал часов показа кампании."""
    Begin: int = None
    End: int = None


class PromotionAdvertsParamNM(BaseEntity):
    """номенклатура кампании."""
    nm: int = None
    active: bool = None


class PromotionAdvertsParam(BaseEntity):
    """Параметры кампании."""
    subjectName: str = None
    active: bool = None
    count: int = None
    intervals: Optional[list[PromotionAdvertsParaminterval]] = []
    price: int = None
    menuId: int = None
    subjectId: int = None
    setId: int = None
    setName: str = None
    menuName: str = None
    nms: Optional[list[PromotionAdvertsParamNM]] = []


class PromotionAdvertsParamsSubject(BaseEntity):
    """Продвигаемый предмет."""
    id_field: int = Field(default=None, alias='id')
    name: str = None


class PromotionAdvertsAutoParamsSet(BaseEntity):
    """Внутренняя (системная) сущность (пол + предмет)."""
    id_field: int = Field(default=None, alias='id')
    name: str = None


class PromotionAdvertsParamsMenu(BaseEntity):
    """Menu."""
    id_field: int = Field(default=None, alias='id')
    name: str = None


class PromotionAdvertsAutoParamsActive(BaseEntity):
    """Зоны показов."""
    carousel: bool = None
    recom: bool = None
    booster: bool = None


class PromotionAdvertsAutoParamsNMCPM(BaseEntity):
    """Ставки номенклатур (артикулов WB)."""
    nm: int = None
    cpm: int = None


class PromotionAdvertsAutoParams(BaseEntity):
    """Параметры автоматической кампании."""
    subject: Optional[PromotionAdvertsParamsSubject] = None
    sets: Optional[list[PromotionAdvertsAutoParamsSet]] = []
    menus: Optional[list[PromotionAdvertsParamsMenu]] = []
    active: Optional[PromotionAdvertsAutoParamsActive] = None
    nmCPM: Optional[list[PromotionAdvertsAutoParamsNMCPM]] = []
    nms: Optional[list[int]] = []
    cpm: int = None


class PromotionAdvertsUnitedParam(BaseEntity):
    """Параметры объедененной кампании."""
    subject: Optional[PromotionAdvertsParamsSubject] = None
    menus: Optional[list[PromotionAdvertsParamsMenu]] = []
    nms: Optional[list[int]] = []
    searchCPM: int = None
    catalogCPM: int = None


class PromotionAdverts(BaseEntity):
    """Информация о кампаниях."""
    advertId: int = None
    type: int = None
    status: int = None
    dailyBudget: int = None
    createTime: str = None
    changeTime: str = None
    startTime: str = None
    endTime: str = None
    name: str = None
    params: Optional[list[PromotionAdvertsParam]] = []
    autoParams: Optional[PromotionAdvertsAutoParams] = None
    unitedParams: Optional[list[PromotionAdvertsUnitedParam]] = []
    searchPluseState: bool = None
