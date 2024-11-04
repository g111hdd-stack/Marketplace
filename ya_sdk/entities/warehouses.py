from typing import Optional
from pydantic import Field

from .gps import GpsDTO
from .base import BaseEntity


class WarehouseAddressDTO(BaseEntity):
    """Адрес склада."""
    city: str
    gps: GpsDTO
    block: Optional[str] = None
    building: Optional[str] = None
    number: Optional[str] = None
    street: Optional[str] = None


class FulfillmentWarehouseDTO(BaseEntity):
    """Склад Маркета (FBY)."""
    id_field: int = Field(default=None, alias='id')
    name: str
    address: WarehouseAddressDTO


class FulfillmentWarehousesDTO(BaseEntity):
    """Список складов Маркета (FBY)."""
    warehouses: list[FulfillmentWarehouseDTO] = []
