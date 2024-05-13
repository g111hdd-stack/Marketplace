from pydantic import Field

from .base import BaseRequest


class FullstatsRequest(BaseRequest):
    """Кампании."""
    id_field: int = Field(alias='id')
    dates: list[str] = []
