from typing import Optional

from .base import BaseEntity


class OrderServiceOrderSearch(BaseEntity):
    shipments: Optional[list[str]] = []
