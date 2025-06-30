
from .base import BaseResponse
from ..entities import CardsList, CardsListCursor


class CardsListResponse(BaseResponse):
    """Возвращает информацию о карточках товаров."""
    cards: list[CardsList]
    cursor: CardsListCursor


