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
        self._analytics_data_api = self._api_factory.get_api(AnalyticsDataResponse)
        self._posting_fbo_list_api = self._api_factory.get_api(PostingFBOListResponse)
        self._posting_fbs_list_api = self._api_factory.get_api(PostingFBSListResponse)
        self._product_info_discounted_api = self._api_factory.get_api(ProductInfoDiscountedResponse)
        self._product_related_sku_get_api = self._api_factory.get_api(ProductRelatedSkuGetResponse)
        self._product_info_stocks_api = self._api_factory.get_api(ProductInfoStocksResponse)
        self._finance_realization_api = self._api_factory.get_api(FinanceRealizationResponse)

    async def get_finance_transaction_list(self, from_field: str, to: str, posting_number: str = "",
                                           operation_type: list[str] = None, transaction_type: str = 'all',
                                           page: int = 1, page_size: int = 1000) -> FinanceTransactionListResponse:
        """
            Список транзакций.

            Тип начисления(некоторые операции могут быть разделены во времени):
                all — все, \n
                orders — заказы, \n
                returns — возвраты и отмены, \n
                services — сервисные сборы, \n
                compensation — компенсация, \n
                transferDelivery — стоимость доставки, \n
                other — прочее.

            Args:
                from_field (str): Начало периода в формате YYYY-MM-DD.
                to (str): Конец периода в формате YYYY-MM-DD.
                posting_number (str, optional): Номер отправления.
                operation_type (bool, optional): Тип Операции.
                transaction_type (str, optional): Тип начисления.
                page (int, optional): Номер страницы, возвращаемой в запросе.
                page_size (int, optional): Количество элементов на странице.
        """
        if operation_type is None:
            operation_type = []
        request = FinanceTransactionListRequest(
            filter=FinanceTransactionListFilter(date=FinanceTransactionListDate(from_field=from_field,
                                                                                to=to),
                                                operation_type=operation_type,
                                                posting_number=posting_number,
                                                transaction_type=transaction_type),
            page=page,
            page_size=page_size
        )
        answer: FinanceTransactionListResponse = await self._finance_transaction_list_api.post(request)

        return answer

    async def get_finance_realization(self, month: int, year: int) -> FinanceRealizationResponse:
        """
            Отчёт о реализации доставленных и возвращённых товаров за месяц.

            Args:
                month (int): Месяц.
                year (int): Год.
        """
        request = FinanceRealizationRequest(month=month, year=year)
        answer: FinanceRealizationResponse = await self._finance_realization_api.post(request)
        return answer

    async def get_posting_fbs(self, posting_number: str, analytics_data: bool = False, barcodes: bool = False,
                              financial_data: bool = False, product_exemplars: bool = False,
                              related_postings: bool = False, translit: bool = False) -> PostingFBSGetResponse:
        """
            Получить информацию схемы доставки FBS об отправлении по идентификатору.

            Args:
                posting_number (str, optional): Номер отправления.
                analytics_data (bool, optional): Добавить в ответ данные аналитики.
                barcodes (bool, optional): Добавить в ответ штрихкоды отправления.
                financial_data (bool, optional): Добавить в ответ финансовые данные.
                product_exemplars (bool, optional): Добавить в ответ данные о продуктах и их экземплярах.
                related_postings (bool, optional): Добавить в ответ номера связанных отправлений.
                    Связанные отправления — те, на которое было разделено родительское отправление при сборке.
                translit (bool, optional): Выполнить транслитерацию возвращаемых значений.
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
            Получить информацию схемы доставки FBO об отправлении по идентификатору.

            Args:
                posting_number (str, optional): Номер отправления.
                analytics_data (bool, optional): Добавить в ответ данные аналитики.
                financial_data (bool, optional): Добавить в ответ финансовые данные.
                translit (bool, optional): Выполнить транслитерацию возвращаемых значений.

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
        """
            Получение списка товаров.

            Фильтр по видимости товара:
                ALL — все товары, кроме архивных. \n
                VISIBLE — товары, которые видны покупателям. \n
                INVISIBLE — товары, которые не видны покупателям. \n
                EMPTY_STOCK — товары, у которых не указано наличие. \n
                NOT_MODERATED — товары, которые не прошли модерацию. \n
                MODERATED — товары, которые прошли модерацию. \n
                DISABLED — товары, которые видны покупателям, но недоступны к покупке. \n
                STATE_FAILED — товары, создание которых завершилось ошибкой. \n
                READY_TO_SUPPLY — товары, готовые к поставке. \n
                VALIDATION_STATE_PENDING — товары, которые проходят проверку валидатором на премодерации. \n
                VALIDATION_STATE_FAIL — товары, которые не прошли проверку валидатором на премодерации. \n
                VALIDATION_STATE_SUCCESS — товары, которые прошли проверку валидатором на премодерации. \n
                TO_SUPPLY — товары, готовые к продаже. \n
                IN_SALE — товары в продаже. \n
                REMOVED_FROM_SALE — товары, скрытые от покупателей. \n
                BANNED — заблокированные товары. \n
                OVERPRICED — товары с завышенной ценой. \n
                CRITICALLY_OVERPRICED — товары со слишком завышенной ценой. \n
                EMPTY_BARCODE — товары без штрихкода. \n
                BARCODE_EXISTS — товары со штрихкодом. \n
                QUARANTINE — товары на карантине после изменения цены более чем на 50%. \n
                ARCHIVED — товары в архиве. \n
                OVERPRICED_WITH_STOCK — товары в продаже со стоимостью выше, чем у конкурентов. \n
                PARTIAL_APPROVED — товары в продаже с пустым или неполным описанием. \n
                IMAGE_ABSENT — товары без изображений. \n
                MODERATION_BLOCK — товары, для которых заблокирована модерация. \n

            Args:
                offer_id (list[str], optional): Список артикулов товаров в системе продавца.
                product_id (list[str], optional): Список id товаров из системы Ozon.
                visibility (str, optional): Фильтр по видимости товара.
                last_id (str, optional): Идентификатор последнего значения на странице.
                limit (int, optional): Количество значений на странице. Минимум — 1, максимум — 1000.
        """
        request = ProductListRequest(filter=ProductListFilter(offer_id=offer_id,
                                                              product_id=product_id,
                                                              visibility=visibility),
                                     last_id=last_id,
                                     limit=limit)
        answer: ProductListResponse = await self._product_list_api.post(request)
        return answer

    async def get_product_info_list(self, offer_id: list[str] = None, product_id: list[str] = None,
                                    sku: list[int] = None) -> ProductInfoListResponse:
        """
            Получение информации о таварах.

            Args:
                offer_id (list[str], optional): Список артикулов товаров в системе продавца.
                product_id (list[str], optional): Список id товаров в системе Ozon.
                sku (list[int], optional): Список sku товаров в системе Ozon.
        """
        request = ProductInfoListRequest(offer_id=offer_id, product_id=product_id, sku=sku)
        answer: ProductInfoListResponse = await self._product_info_list_api.post(request)
        return answer

    async def get_products_info_attributes(self, offer_id: list[str] = None, product_id: list[str] = None,
                                           sku: list[str] = None, visibility: str = 'ALL', last_id: str = None,
                                           limit: int = 100, sort_by: str = None, sort_dir: str = None) \
            -> ProductsInfoAttributesResponse:
        """
            Получаем описание характеристик товара.

            Args:
                offer_id (list[str], optional): Список артикулов товаров в системе продавца.
                product_id (list[str], optional): Список id товаров в системе Ozon.
                sku (list[str], optional): Список sku товаров в системе Ozon.
                visibility (str, optional): Фильтр по видимости товара.. Default ALL.
                last_id (str, optional): Идентификатор последнего значения на странице.
                limit (int, optional): Количество значений на странице. Минимум — 1, максимум — 1000.
                sort_by (str, optional): Параметр, по которому товары будут отсортированы.
                sort_dir (str, optional): Направление сортировки.
        """
        request = ProductsInfoAttributesRequest(filter=ProductsInfoAttributesFilter(offer_id=offer_id,
                                                                                    product_id=product_id,
                                                                                    sku=sku,
                                                                                    visibility=visibility),
                                                last_id=last_id,
                                                limit=limit,
                                                sort_by=sort_by,
                                                sort_dir=sort_dir)
        answer: ProductsInfoAttributesResponse = await self._products_info_attributes_api.post(request)
        return answer

    async def get_analytics_data(self, date_from: str, date_to: str, dimension: list[str] = None,
                                 filters: list[AnalyticsDataFilter] = None, limit: int = 100,
                                 metrics: list[str] = None, offset: int = 0,
                                 sort: list[AnalyticsDataSort] = None) -> AnalyticsDataResponse:
        """
            Получение аналитических данных.

            Способы группировки, доступные всем продавцам:
                unknownDimension — неизвестное измерение, \n
                sku — идентификатор товара, \n
                spu — идентификатор товара, \n
                day — день, \n
                week — неделя, \n
                month — месяц.

            Способы группировки, доступные только продавцам с Premium-подпиской:
                year — год, \n
                category1 — категория первого уровня, \n
                category2 — категория второго уровня, \n
                category3 — категория третьего уровня, \n
                category4 — категория четвертого уровня, \n
                brand — бренд, \n
                modelID — модель.

            Args:
                date_from (str): Дата, с которой будут данные в отчёте.
                date_to (str): Дата, по которую будут данные в отчёте.
                dimension (list[str], optional): Группировка данных в отчёте.
                filters (list[AnalyticsDataFilter], optional): Фильтры.
                limit (int. optional): Количество значений в ответе. Минимум — 1, максимум — 1000.
                metrics (list[str], optional): Список метриĸ, по ĸоторым будет сформирован отчёт. Укажите до 14 метрик.
                offset (int, optional): Количество элементов, которое будет пропущено в ответе.
                sort (list[AnalyticsDataSort], optional): Настройки сортировки отчёта.
        """
        request = AnalyticsDataRequest(date_from=date_from,
                                       date_to=date_to,
                                       dimension=dimension,
                                       filters=filters,
                                       limit=limit,
                                       metrics=metrics,
                                       offset=offset,
                                       sort=sort)
        answer: AnalyticsDataResponse = await self._analytics_data_api.post(request)
        return answer

    async def get_posting_fbo_list(self, since: str, to: str, order_by: str = 'asc', status: str = '',
                                   limit: int = 1000, offset: int = 0, translit: bool = False,
                                   analytics_data: bool = False,
                                   financial_data: bool = False) -> PostingFBOListResponse:
        """
            Получить информацию по отправлениям схемы FBO.

            Направление сортировки:
                asc — по возрастанию, \n
                desc — по убыванию.
            Статус отправления:
                awaiting_packaging — ожидает упаковки, \n
                awaiting_deliver — ожидает отгрузки, \n
                delivering — доставляется, \n
                delivered — доставлено, \n
                cancelled — отменено. \n

            Args:
                since (str): Начало периода в формате YYYY-MM-DD.
                to (str): Конец периода в формате YYYY-MM-DD.
                order_by (str, optional): Направление сортировки.
                status (str, optional): Статус отправления.
                limit (int, optional): Количество значений в ответе. Минимум — 1, максимум — 1000.
                offset (int, optional): Количество элементов, которое будет пропущено в ответе.
                translit (bool, optional): Выполнить транслитерацию возвращаемых значений.
                analytics_data (bool, optional): Добавить в ответ данные аналитики.
                financial_data (bool, optional): Добавить в ответ финансовые данные.
        """
        request = PostingFBOListRequest(order_by=order_by,
                                        filter=PostingFBOListFilter(since=since,
                                                                    status=status,
                                                                    to=to),
                                        limit=limit,
                                        offset=offset,
                                        translit=translit,
                                        with_field=PostingFBOListWith(analytics_data=analytics_data,
                                                                      financial_data=financial_data))
        answer: PostingFBOListResponse = await self._posting_fbo_list_api.post(request)
        return answer

    async def get_posting_fbs_list(self, since: str, to: str, order_by: str = 'asc',
                                   delivery_method_id: list[int] = None, order_id: int = None,
                                   provider_id: list[int] = None, status: str = '', warehouse_id: list[int] = None,
                                   from_last_changed_status_date: str = None,
                                   to_last_changed_status_date: str = None, limit: int = 1000, offset: int = 0,
                                   analytics_data: bool = False, barcodes: bool = False,
                                   financial_data: bool = False, translit: bool = False) -> PostingFBSListResponse:
        """
            Получить информацию по отправлениям схемы FBO.

            Направление сортировки:
                asc — по возрастанию, \n
                desc — по убыванию.
            Статус отправления:
                awaiting_packaging — ожидает упаковки, \n
                awaiting_deliver — ожидает отгрузки, \n
                delivering — доставляется, \n
                delivered — доставлено, \n
                cancelled — отменено. \n

            Args:
                since (str): Начало периода в формате YYYY-MM-DD.
                to (str): Конец периода в формате YYYY-MM-DD.
                order_by (str, optional): Направление сортировки.
                delivery_method_id (list[int], optional): Идентификатор способа доставки.
                order_id (int, optional): Идентификатор заказа.
                provider_id (list[int], optional): Идентификатор службы доставки.
                status (str, optional): Статус отправления.
                warehouse_id (list[int], optional): Идентификатор склада.
                from_last_changed_status_date (str, optional): Дата начала периода изменения статуса
                                                               в формате YYYY-MM-DD.
                to_last_changed_status_date (str, optional): Дата окончания периода изменения статуса
                                                             в формате YYYY-MM-DD.
                limit (int, optional): Количество значений в ответе. Минимум — 1, максимум — 1000.
                offset (int, optional): Количество элементов, которое будет пропущено в ответе.
                analytics_data (bool, optional): Добавить в ответ данные аналитики.
                barcodes (bool, optional): Добавить в ответ штрихкоды отправления.
                financial_data (bool, optional): Добавить в ответ финансовые данные.
                translit (bool, optional): Выполнить транслитерацию возвращаемых значений.
        """
        request = PostingFBSListRequest(
            order_by=order_by,
            filter=PostingFBSListFilter(delivery_method_id=delivery_method_id or [],
                                        order_id=order_id,
                                        provider_id=provider_id or [],
                                        since=since,
                                        status=status,
                                        warehouse_id=warehouse_id or [],
                                        to=to,
                                        last_changed_status_date=PostingFBSListFilterLastChangedStatusDate(
                                            from_field=from_last_changed_status_date,
                                            to=to_last_changed_status_date)),
            limit=limit,
            offset=offset,
            with_field=PostingFBSListWith(analytics_data=analytics_data,
                                          barcodes=barcodes,
                                          financial_data=financial_data,
                                          translit=translit))
        answer: PostingFBSListResponse = await self._posting_fbs_list_api.post(request)
        return answer

    async def get_product_info_discounted(self, discounted_skus: list[str]) -> ProductInfoDiscountedResponse:
        """
            Метод для получения информации о состоянии и дефектах уценённого товара по его SKU.
            Также метод возвращает SKU основного товара.

            Args:
                discounted_skus (list[str): Список SKU уценённых товаров.
        """
        request = ProductInfoDiscountedRequest(discounted_skus=discounted_skus)
        answer: ProductInfoDiscountedResponse = await self._product_info_discounted_api.post(request)
        return answer

    async def get_product_related_sku_get(self, skus: list[str]) -> ProductRelatedSkuGetResponse:
        """
            Метод для получения единого SKU по старым идентификаторам SKU FBS и SKU FBO.
            В ответе будут все SKU, связанные с переданными.

            Передавайте до 200 SKU в одном запросе.

            Args:
                skus (list[str): Список SKU.
        """
        request = ProductRelatedSkuGetRequest(sku=skus)
        answer: ProductRelatedSkuGetResponse = await self._product_related_sku_get_api.post(request)
        return answer

    async def get_product_info_stocks(self, offer_id: list[str] = None, product_id: list[str] = None,
                                      visibility: str = 'ALL', cursor: str = None,
                                      limit: int = 100) -> ProductInfoStocksResponse:
        """
            Получение остатков товаров на складе.

            Фильтр по видимости товара:
                ALL — все товары, кроме архивных. \n
                VISIBLE — товары, которые видны покупателям. \n
                INVISIBLE — товары, которые не видны покупателям. \n
                EMPTY_STOCK — товары, у которых не указано наличие. \n
                NOT_MODERATED — товары, которые не прошли модерацию. \n
                MODERATED — товары, которые прошли модерацию. \n
                DISABLED — товары, которые видны покупателям, но недоступны к покупке. \n
                STATE_FAILED — товары, создание которых завершилось ошибкой. \n
                READY_TO_SUPPLY — товары, готовые к поставке. \n
                VALIDATION_STATE_PENDING — товары, которые проходят проверку валидатором на премодерации. \n
                VALIDATION_STATE_FAIL — товары, которые не прошли проверку валидатором на премодерации. \n
                VALIDATION_STATE_SUCCESS — товары, которые прошли проверку валидатором на премодерации. \n
                TO_SUPPLY — товары, готовые к продаже. \n
                IN_SALE — товары в продаже. \n
                REMOVED_FROM_SALE — товары, скрытые от покупателей. \n
                BANNED — заблокированные товары. \n
                OVERPRICED — товары с завышенной ценой. \n
                CRITICALLY_OVERPRICED — товары со слишком завышенной ценой. \n
                EMPTY_BARCODE — товары без штрихкода. \n
                BARCODE_EXISTS — товары со штрихкодом. \n
                QUARANTINE — товары на карантине после изменения цены более чем на 50%. \n
                ARCHIVED — товары в архиве. \n
                OVERPRICED_WITH_STOCK — товары в продаже со стоимостью выше, чем у конкурентов. \n
                PARTIAL_APPROVED — товары в продаже с пустым или неполным описанием. \n
                IMAGE_ABSENT — товары без изображений. \n
                MODERATION_BLOCK — товары, для которых заблокирована модерация. \n

            Args:
                offer_id (list[str], optional): Список артикулов товаров в системе продавца.
                product_id (list[str], optional): Список id товаров из системы Ozon.
                visibility (str, optional): Фильтр по видимости товара.
                cursor (str, optional): Идентификатор последнего значения на странице.
                limit (int, optional): Количество значений на странице. Минимум — 1, максимум — 1000.
        """
        request = ProductInfoStocksRequest(filter=ProductInfoStocksFilter(offer_id=offer_id,
                                                                          product_id=product_id,
                                                                          visibility=visibility),
                                           cursor=cursor,
                                           limit=limit)
        answer: ProductInfoStocksResponse = await self._product_info_stocks_api.post(request)
        return answer


class OzonPerformanceAPI:

    def __init__(self, client_id: str, client_secret: str):
        """
            Args:
                client_id (_type_): ID рекламного кабинета
                client_secret (_type_): SECRET KEY рекламного кабинета
        """
        self._engine = OzonPerformanceAsyncEngine(client_id=client_id, client_secret=client_secret)
        self._api_factory = OzonPerformanceAPIFactory(self._engine)

        self._client_campaign_api = self._api_factory.get_api(ClientCampaignResponse)
        self._client_statistics_json_api = self._api_factory.get_api(ClientStatisticsJSONResponse)
        self._client_statistics_daily_json_api = self._api_factory.get_api(ClientStatisticsDailyJSONResponse)
        self._client_statistics_uuid_api = self._api_factory.get_api(ClientStatisticsUUIDResponse)
        self._client_statistics_report_api = self._api_factory.get_api(ClientStatisticsReportResponse)
        self._client_campaign_objects_api = self._api_factory.get_api(ClientCampaignObjectsResponse)
        self._client_campaign_search_promo_products_api = self._api_factory.get_api(
            ClientCampaignSearchPromoProductsResponse)

    async def get_client_campaign(self, campaign_ids: list[str] = None, adv_object_type: str = None,
                                  state: str = None) -> ClientCampaignResponse:
        """
            Получения списка рекламных компаний.

            Тип рекламируемой кампании:
                SKU — Трафареты; \n
                BANNER — Баннерная рекламная кампания; \n
                BRAND_SHELF — Брендовая полка; \n
                SEARCH_PROMO — Продвижение в поиске; \n
                VIDEO_BANNER — Видео баннер; \n
                ACTION — Акция.

            Состояние кампании:
                CAMPAIGN_STATE_RUNNING — активная кампания; \n
                CAMPAIGN_STATE_PLANNED — кампания, сроки проведения которой ещё не наступили; \n
                CAMPAIGN_STATE_STOPPED — кампания, сроки проведения которой завершились; \n
                CAMPAIGN_STATE_INACTIVE — кампания, остановленная владельцем; \n
                CAMPAIGN_STATE_ARCHIVED — архивная кампания; \n
                CAMPAIGN_STATE_MODERATION_DRAFT — отредактированная кампания до отправки на модерацию; \n
                CAMPAIGN_STATE_MODERATION_IN_PROGRESS — кампания, отправленная на модерацию; \n
                CAMPAIGN_STATE_MODERATION_FAILED — кампания, непрошедшая модерацию; \n
                CAMPAIGN_STATE_FINISHED — кампания завершена, дата окончания в прошлом, такую кампанию нельзя изменить,
                можно только клонировать или создать новую.

            Args:
                campaign_ids (list[str], optional): Список идентификаторов кампаний,
                                                    для которых необходимо вывести информацию.
                adv_object_type (str, optional): Тип рекламируемой кампании.
                state (str, optional): Состояние кампании.
        """
        request = ClientCampaignRequest(campaignIds=campaign_ids, advObjectType=adv_object_type, state=state)
        answer: ClientCampaignResponse = await self._client_campaign_api.get(request)
        return answer

    async def get_client_statistics_json(self, campaigns: list[str], from_field: str = None, to: str = None,
                                         date_from: str = None, date_to: str = None, group_by: str = None) \
            -> ClientStatisticsJSONResponse:
        """
            Получение статистики по рекламной компании.

            Тип группировки по времени:
                DATE — группировка по дате (по дням); \n
                START_OF_WEEK — группировка по неделям; \n
                START_OF_MONTH — группировка по месяцам.

            Args:
                campaigns (list[str], optional): Список идентификаторов кампаний,
                                                 для которых необходимо подготовить отчёт.
                from_field (str, optional): Начальная дата периода отчёта в формате RFC 3339.
                                            Максимальный период — 62 дня.
                to (str, optional): Конечная дата периода отчёта в формате RFC 3339. Максимальный период — 62 дня.
                date_from (str, optional): Начальная дата периода отчёта в формате ГГГГ-ММ-ДД.
                date_to (str, optional): Конечная дата периода отчёта в формате ГГГГ-ММ-ДД.
                group_by (str, optional): Тип группировки по времени.. Default None.
        """
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
        """
            Получение дневной статистики по рекламной компании.

            Args:
                campaigns (list[str], optional): Список идентификаторов кампаний,
                                                 для которых необходимо подготовить отчёт.
                date_from (str, optional): Начальная дата периода отчёта в формате ГГГГ-ММ-ДД.
                date_to (str, optional): Конечная дата периода отчёта в формате ГГГГ-ММ-ДД.
        """
        request = ClientStatisticsDailyJSONRequest(campaigns=campaigns,
                                                   dateFrom=date_from,
                                                   dateTo=date_to)
        answer: ClientStatisticsDailyJSONResponse = await self._client_statistics_daily_json_api.get(request)
        return answer

    async def get_client_statistics_uuid(self, uuid: str) -> ClientStatisticsUUIDResponse:
        """
            Cтатус отчёта.

            Args:
                uuid (str): UUID отчета.
        """
        request = ClientStatisticsUUIDRequest()
        answer: ClientStatisticsUUIDResponse = await self._client_statistics_uuid_api.get(request,
                                                                                          format_dict={'UUID': uuid})
        return answer

    async def get_client_statistics_report(self, uuid: str) -> ClientStatisticsReportResponse:
        """
            Получение отчета.

            Args:
                uuid (str): UUID отчета.
        """
        request = ClientStatisticsReportRequest(UUID=uuid)
        answer: ClientStatisticsReportResponse = await self._client_statistics_report_api.get(request)
        return answer

    async def get_client_campaign_objects(self, campaign_id: str) -> ClientCampaignObjectsResponse:
        """
            Получение отчета.

            Args:
                campaign_id (str): ID РК.
        """
        request = ClientCampaignObjectsRequest()
        answer: ClientCampaignObjectsResponse = await self._client_campaign_objects_api.get(
            request, format_dict={'campaignId': campaign_id})
        return answer

    async def get_client_campaign_search_promo_products(self,
                                                        campaign_id: str) -> ClientCampaignSearchPromoProductsResponse:
        """
            Получение отчета.

            Args:
                campaign_id (str): ID РК.
        """
        request = ClientCampaignObjectsRequest()
        answer: ClientCampaignSearchPromoProductsResponse = await self._client_campaign_search_promo_products_api.get(
            request, format_dict={'campaignId': campaign_id})
        return answer
