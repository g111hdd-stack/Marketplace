from .requests import *
from .response import *
from .core import OzonAsyncEngine, OzonPerformanceAsyncEngine
from .ozon_endpoints_list import OzonAPIFactory, OzonPerformanceAPIFactory


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
        self._product_list_api = self._api_factory.get_api(ProductListResponse)
        self._product_info_list_api = self._api_factory.get_api(ProductInfoListResponse)
        self._products_info_attributes_api = self._api_factory.get_api(ProductsInfoAttributesResponse)

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

    async def get_product_list(self, offer_id: list[str] = None, product_id: list[str] = None, visibility: str = 'ALL',
                               last_id: str = None, limit: int = 100) -> ProductListResponse:
        request = ProductListRequest(filter=ProductListFilter(offer_id=offer_id,
                                                              product_id=product_id,
                                                              visibility=visibility),
                                     last_id=last_id,
                                     limit=limit)
        answer: ProductListResponse = await self._product_list_api.post(request)
        return answer

    async def get_product_info_list(self, offer_id: list[str] = None, product_id: list[int] = None,
                                    sku: list[int] = None) -> ProductInfoListResponse:
        request = ProductInfoListRequest(offer_id=offer_id, product_id=product_id, sku=sku)
        answer: ProductInfoListResponse = await self._product_info_list_api.post(request)
        return answer

    async def get_products_info_attributes(self, offer_id: list[str] = None, product_id: list[str] = None,
                                           visibility: str = 'ALL', last_id: str = None, limit: int = 100,
                                           sort_by: str = None, sort_dir: str = None) \
            -> ProductsInfoAttributesResponse:
        request = ProductsInfoAttributesRequest(filter=ProductsInfoAttributesFilter(offer_id=offer_id,
                                                                                    product_id=product_id,
                                                                                    visibility=visibility),
                                                last_id=last_id,
                                                limit=limit,
                                                sort_by=sort_by,
                                                sort_dir=sort_dir)
        answer: ProductsInfoAttributesResponse = await self._products_info_attributes_api.post(request)
        return answer


class OzonPerformanceAPI:
    def __init__(self, client_id: str, client_secret: str):
        """
            Args:
                client_id (_type_): ID кабинета
                client_secret (_type_): API KEY кабинета
        """
        self._engine = OzonPerformanceAsyncEngine(client_id=client_id, client_secret=client_secret)
        self._api_factory = OzonPerformanceAPIFactory(self._engine)

        self._client_campaign_api = self._api_factory.get_api(ClientCampaignResponse)
        self._client_statistics_json_api = self._api_factory.get_api(ClientStatisticsJSONResponse)
        self._client_statistics_daily_json_api = self._api_factory.get_api(ClientStatisticsDailyJSONResponse)

    async def get_client_campaign(self, campaign_ids: list[str] = None, adv_object_type: str = None,
                                  state: str = None) -> ClientCampaignResponse:
        request = ClientCampaignRequest(campaignIds=campaign_ids, advObjectType=adv_object_type, state=state)
        answer: ClientCampaignResponse = await self._client_campaign_api.get(request)
        return answer

    async def get_client_statistics_json(self, campaigns: list[str], from_field: str = None, to: str = None,
                                         date_from: str = None, date_to: str = None, group_by: str = None) \
            -> ClientStatisticsJSONResponse:
        request = ClientStatisticsJSONRequest(campaigns=campaigns,
                                              from_field=from_field,
                                              to=to,
                                              dateFrom=date_from,
                                              dateTo=date_to,
                                              groupBy=group_by)
        answer: ClientStatisticsJSONResponse = await self._client_statistics_json_api.post(request)
        return answer

    async def get_client_statistics_daily_json(self, campaigns: list[str] = None, date_from: str = None,
                                               date_to: str = None) -> ClientStatisticsDailyJSONResponse:
        request = ClientStatisticsDailyJSONRequest(campaigns=campaigns,
                                                   dateFrom=date_from,
                                                   dateTo=date_to)
        answer: ClientStatisticsDailyJSONResponse = await self._client_statistics_daily_json_api.get(request)
        return answer
