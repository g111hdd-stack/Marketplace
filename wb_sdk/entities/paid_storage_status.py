from pydantic import Field

from .base import BaseEntity


class PaidStorageStatus(BaseEntity):
    id_field: str = Field(default=None, alias='id')
    status: str = None
    