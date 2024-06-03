from pydantic import Field

from .base import BaseEntity


class FlippingPagerDTO(BaseEntity):
    """Модель для пагинации."""
    total: int = None
    from_field: int = Field(default=None, alias='from')
    to: int = None
    currentPage: int = None
    pagesCount: int = None
    pageSize: int = None
