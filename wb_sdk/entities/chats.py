from typing import Optional

from .base import BaseEntity


class ChatsGoodCard(BaseEntity):
    """Информация о заказе."""
    date: Optional[str] = None
    nmID: Optional[int] = None
    price: Optional[int] = None
    priceCurrency: Optional[str] = None
    rid: Optional[str] = None
    size: Optional[str] = None

class ChatsLastMessage(BaseEntity):
    """Последнее сообщение в чате."""
    text: Optional[str] = None
    addTimestamp: Optional[int] = None

class Chats(BaseEntity):
    """Чат."""
    chatID: Optional[str] = None
    replySign: Optional[str] = None
    clientName: Optional[str] = None
    goodCard: Optional[ChatsGoodCard] = None
    lastMessage: Optional[ChatsLastMessage] = None
