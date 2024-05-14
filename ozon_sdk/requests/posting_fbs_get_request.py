from pydantic import Field

from .base import BaseRequest


class PostingFBSGetWith(BaseRequest):
    """
        Дополнительные поля, которые нужно добавить в ответ.

        Аргументы:
            analytics_data (bool, optional): Добавить в ответ данные аналитики.. Default to False. \n
            barcodes (bool, optional): Добавить в ответ штрихкоды отправления.. Default to False. \n
            financial_data (bool, optional): Добавить в ответ финансовые данные.. Default to False. \n
            product_exemplars (bool, optional): Добавить в ответ данные о продуктах и их экземплярах.. Default to False. \n
            related_postings (bool, optional): Добавить в ответ номера связанных отправлений.
            Связанные отправления — те, на которое было разделено родительское отправление при сборке.. Default to False. \n
            translit (bool, optional): Выполнить транслитерацию возвращаемых значений.. Default to False.
    """
    analytics_data: bool = False
    barcodes: bool = False
    financial_data: bool = False
    product_exemplars: bool = False
    related_postings: bool = False
    translit: bool = False


class PostingFBSGetRequest(BaseRequest):
    """
        Возвращает информацию об отправлении по его идентификатору.

        Аргументы:
            posting_number (str): Идентификатор отправления. \n
            with_field (PostingFBSGetWith, optional): Дополнительные поля, которые нужно добавить в ответ.
    """
    posting_number: str
    with_field: PostingFBSGetWith = Field(default=PostingFBSGetWith, serialization_alias='with')
