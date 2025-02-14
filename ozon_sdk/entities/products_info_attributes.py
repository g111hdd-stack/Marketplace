from typing import Optional
from pydantic import Field

from .base import BaseEntity


class ProductsInfoAttributeValue(BaseEntity):
    """Массив характеристик товара."""
    dictionary_value_id: int = None
    value: str = None


class ProductsInfoAttribute(BaseEntity):
    """Массив характеристик товара."""
    attribute_id: int = None
    complex_id: int = None
    values: Optional[list[ProductsInfoAttributeValue]] = []


class ProductsInfoAttributesAttributes(BaseEntity):
    """Массив вложенных характеристик."""
    attributes: Optional[list[ProductsInfoAttribute]] = []


class ProductsInfoAttributesModelInfo(BaseEntity):
    """Информация о модели."""
    model_id: int = None
    count: int = None

    class Config:
        protected_namespaces = ()


class ProductsInfoAttributesPDF(BaseEntity):
    """Массив PDF-файлов."""
    file_name: str = None
    name: str = None


class ProductsInfoAttributes(BaseEntity):
    """Результаты запроса."""
    attributes: Optional[list[ProductsInfoAttribute]] = []
    barcode: str = None
    description_category_id: int = None
    color_image: str = None
    complex_attributes: Optional[list[ProductsInfoAttributesAttributes]] = []
    depth: int = None
    dimension_unit: str = None
    height: int = None
    id_field: int = Field(default=None, alias='id')
    images: Optional[list[str]] = []
    model_info: Optional[ProductsInfoAttributesModelInfo] = None
    name: str = None
    offer_id: str = None
    primary_image: str = None
    type_id: int = None
    pdf_list: Optional[list[ProductsInfoAttributesPDF]] = []
    weight: int = None
    weight_unit: str = None
    width: int = None

    class Config:
        protected_namespaces = ()
