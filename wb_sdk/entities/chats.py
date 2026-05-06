from .base import BaseEntity


class ChatsGoodCard(BaseEntity):
    """Информация о заказе."""
    date: str = None
    nmID: int = None
    price: int = None
    priceCurrency: str = None
    rid: str = None
    size: str = None

class ChatsLastMessage(BaseEntity):
    """Последнее сообщение в чате."""
    text: str = None
    addTimestamp: int = None

class Chats(BaseEntity):
    """Чат."""
    chatID: str = None
    replySign: str = None
    clientName: str = None
    goodCard: ChatsGoodCard = None
    lastMessage: ChatsLastMessage = None
