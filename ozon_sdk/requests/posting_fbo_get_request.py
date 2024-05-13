from pydantic import Field

from .base import BaseRequest


class PostingFBOGetWith(BaseRequest):
    """
        Дополнительные поля, которые нужно добавить в ответ.

        Аргументы:
            analytics_data (bool, optional): Добавить в ответ данные аналитики.. Default to False. \n
            financial_data (bool, optional): Добавить в ответ финансовые данные.. Default to False.
    """
    analytics_data: bool = False
    financial_data: bool = False


class PostingFBOGetRequest(BaseRequest):
    """
        Возвращает информацию об отправлении по его идентификатору.

        Аргументы:
            posting_number (str): Идентификатор отправления. \n
            translit (bool, optional): Если включена транслитерация адреса из кириллицы в латиницу — true.. Default to False. \n
            with_field (PostingFBSGetWith, optional): Дополнительные поля, которые нужно добавить в ответ.
    """
    posting_number: str
    translit: bool = False
    with_field: PostingFBOGetWith = Field(default=PostingFBOGetWith, alias='with')
