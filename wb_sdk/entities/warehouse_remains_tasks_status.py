from pydantic import Field

from .base import BaseEntity


class WarehouseRemainsTasksStatus(BaseEntity):
    """Статус отчёт по остаткам на складах."""
    id_field: str = Field(alias='id')
    status: str
