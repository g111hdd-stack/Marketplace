from typing import Optional
from pydantic import Field

from .base import BaseEntity


class ProductsInfoAttributeValue(BaseEntity):
    dictionary_value_id: int = None
    value: str = None


class ProductsInfoAttribute(BaseEntity):
    attribute_id: int = None
    complex_id: int = None
    values: Optional[list[ProductsInfoAttributeValue]] = []


class ProductsInfoAttributesAttributes(BaseEntity):
    attributes: Optional[list[ProductsInfoAttribute]] = []


class ProductsInfoAttributesImage(BaseEntity):
    default: bool = None
    file_name: str = None
    index: int = None


class ProductsInfoAttributesImage360(BaseEntity):
    file_name: str = None
    index: int = None


class ProductsInfoAttributesPDF(BaseEntity):
    file_name: str = None
    index: int = None
    name: str = None


class ProductsInfoAttributes(BaseEntity):
    attributes: Optional[list[ProductsInfoAttribute]] = []
    barcode: str = None
    category_id: int = None
    description_category_id: int = None
    color_image: str = None
    complex_attributes: Optional[list[ProductsInfoAttributesAttributes]] = []
    depth: int = None
    dimension_unit: str = None
    height: int = None
    id_field: int = Field(default=None, alias='id')
    image_group_id: str = None
    images: Optional[list[ProductsInfoAttributesImage]] = []
    images360: Optional[list[ProductsInfoAttributesImage360]] = []
    name: str = None
    offer_id: str = None
    pdf_list: Optional[list[ProductsInfoAttributesPDF]] = []
    weight: int = None
    weight_unit: str = None
    width: int = None
