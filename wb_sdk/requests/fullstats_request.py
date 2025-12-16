from pydantic import Field

from .base import BaseRequest


class FullstatsRequest(BaseRequest):
    """Кампании."""
    ids: str
    beginDate: str
    endDate: str