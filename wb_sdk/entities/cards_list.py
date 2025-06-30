from pydantic import Field
from typing import Any, Optional

from .base import BaseEntity


class CardsListPhoto(BaseEntity):
    """Массив фото"""
    big: Optional[str] = None
    c246x328: Optional[str] = None
    c516x688: Optional[str] = None
    square: Optional[str] = None
    tm: Optional[str] = None


class CardsListDimensions(BaseEntity):
    """Габариты и вес товара с упаковкой, см и кг."""
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    weightBrutto: Optional[float] = None
    isValid: Optional[bool] = None


class CardsListCharacteristics(BaseEntity):
    """Характеристики."""
    id_field: Optional[int] = Field(default=None, alias='id')
    name: Optional[str] = None
    value: Optional[Any] = None


class CardsListSizes(BaseEntity):
    """Размеры товара."""
    chrtID: Optional[int] = None
    techSize: Optional[str] = None
    wbSize: Optional[str] = None
    skus: Optional[list[str]] = []


class CardsListTags(BaseEntity):
    """Ярлыки."""
    id_field: Optional[int] = Field(default=None, alias='id')
    name: Optional[str] = None
    color: Optional[str] = None


class CardsList(BaseEntity):
    """Информация о карточке товара."""
    nmID: int
    imtID: int
    nmUUID: str
    subjectID: int
    subjectName: str
    vendorCode: str
    brand: str
    title: str
    description: Optional[str] = None
    needKiz: bool
    photos: Optional[list[CardsListPhoto]] = []
    video: Optional[str] = None
    dimensions: Optional[CardsListDimensions] = None
    characteristics: Optional[list[CardsListCharacteristics]] = []
    sizes: Optional[list[CardsListSizes]] = []
    tags: Optional[list[CardsListTags]] = []
    createdAt: str
    updatedAt: str


class CardsListCursor(BaseEntity):
    """Пагинатор."""
    updatedAt: Optional[str] = None
    nmID: Optional[int] = None
    total: Optional[int] = None
