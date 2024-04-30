from .requests import FinanceTransactionListRequest, PostingFBSGetRequest, PostingFBOGetRequest, \
    FinanceTransactionListFilter, FinanceTransactionListDate, PostingFBSGetWith, PostingFBOGetWith
from .response import FinanceTransactionListResponse, PostingFBSGetResponse, PostingFBOGetResponse
from .core import OzonAsyncEngine
from .ozon_endpoints_list import OzonAPIFactory


class OzonApi:

    def __init__(self, client_id: str, api_key: str):
        """
            Args:
                client_id (_type_): ID кабинета
                api_key (_type_): API KEY кабинета
        """

        self._engine = OzonAsyncEngine(client_id=client_id, api_key=api_key)
        self._api_factory = OzonAPIFactory(self._engine)

        self._finance_transaction_list_api = self._api_factory.get_api(FinanceTransactionListResponse)
        self._posting_fbs_get_api = self._api_factory.get_api(PostingFBSGetResponse)
        self._posting_fbo_get_api = self._api_factory.get_api(PostingFBOGetResponse)

    async def get_finance_transaction_list(self, from_field: str, to: str, posting_number: str = "",
                                           operation_type: list[str] = None, transaction_type: str = 'all', page: int = 1,
                                           page_size: int = 1000) -> FinanceTransactionListResponse:
        """
            Список транзакций

            Args:
                from_field (str): Начало периода в формате YYYY-MM-DD.
                to (str): Конец периода в формате YYYY-MM-DD.
                posting_number (str, optional): Номер отправления.
                operation_type (bool, optional):
                transaction_type (str, optional): Тип начисления(некоторые операции могут быть разделены во времени):
                    all — все,
                    orders — заказы,
                    returns — возвраты и отмены,
                    services — сервисные сборы,
                    compensation — компенсация,
                    transferDelivery — стоимость доставки,
                    other — прочее.. Defaults to all.
                page (int, optional): Номер страницы, возвращаемой в запросе.. Defaults to 1.
                page_size (int, optional): Количество элементов на странице.. Defaults to 1000

                Returns:
                    FinanceTransactionListResponse
        """
        if operation_type is None:
            operation_type = []
        request = FinanceTransactionListRequest(filter=FinanceTransactionListFilter(date=FinanceTransactionListDate(from_field=from_field,
                                                                                                                    to=to),
                                                                                    operation_type=operation_type,
                                                                                    posting_number=posting_number,
                                                                                    transaction_type=transaction_type),
                                                page=page,
                                                page_size=page_size)
        answer: FinanceTransactionListResponse = await self._finance_transaction_list_api.post(request)

        return answer

    async def get_posting_fbs(self, posting_number: str, analytics_data: bool = False, barcodes: bool = False,
                              financial_data: bool = False, product_exemplars: bool = False,
                              related_postings: bool = False, translit: bool = False) -> PostingFBSGetResponse:
        """
            Получить информацию схемы доставки FBS об отправлении по идентификатору

            Args:
                posting_number (str, optional): Номер отправления.
                analytics_data (bool, optional): Добавить в ответ данные аналитики.. Defaults to False.
                barcodes (bool, optional): Добавить в ответ штрихкоды отправления.. Defaults to False.
                financial_data (bool, optional): Добавить в ответ финансовые данные.. Defaults to False.
                product_exemplars (bool, optional): Добавить в ответ данные о продуктах и их экземплярах.. Defaults to False.
                related_postings (bool, optional): Добавить в ответ номера связанных отправлений.
                    Связанные отправления — те, на которое было разделено родительское отправление при сборке..
                    Defaults to False.
                translit (bool, optional): Выполнить транслитерацию возвращаемых значений.. Defaults to False.

            Returns:
                PostingFBSGetResponse
        """
        request = PostingFBSGetRequest(posting_number=posting_number,
                                       with_field=PostingFBSGetWith(analytics_data=analytics_data,
                                                                    barcodes=barcodes,
                                                                    financial_data=financial_data,
                                                                    product_exemplars=product_exemplars,
                                                                    related_postings=related_postings,
                                                                    translit=translit))
        answer: PostingFBSGetResponse = await self._posting_fbs_get_api.post(request)
        return answer

    async def get_posting_fbo(self, posting_number: str, analytics_data: bool = False, financial_data: bool = False,
                              translit: bool = False) -> PostingFBOGetResponse:
        """
            Получить информацию схемы доставки FBO об отправлении по идентификатору

            Args:
                posting_number (str, optional): Номер отправления.
                analytics_data (bool, optional): Добавить в ответ данные аналитики.. Defaults to False.
                financial_data (bool, optional): Добавить в ответ финансовые данные.. Defaults to False.
                translit (bool, optional): Выполнить транслитерацию возвращаемых значений.. Defaults to False.

            Returns:
                PostingFBOGetResponse
        """
        request = PostingFBOGetRequest(posting_number=posting_number,
                                       translit=translit,
                                       with_field=PostingFBOGetWith(analytics_data=analytics_data,
                                                                    financial_data=financial_data))
        answer: PostingFBOGetResponse = await self._posting_fbo_get_api.post(request)
        return answer
