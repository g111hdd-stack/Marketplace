from typing import Type

from .response import *
from .ozon_async_api import OzonAsyncApi
from .core import OzonAsyncEngine, OzonPerformanceAsyncEngine


class OzonAPIFactory:
    """Фабрика для endpoint'ов апи. Получение инстанса апи для каждого типа возвращаемого значения."""

    api_list: dict[Type[BaseResponse], str] = {
        FinanceTransactionListResponse: '/v3/finance/transaction/list',
        PostingFBSGetResponse: '/v3/posting/fbs/get',
        PostingFBOGetResponse: '/v2/posting/fbo/get',
        ProductListResponse: '/v2/product/list',
        ProductInfoListResponse: '/v2/product/info/list',
        ProductsInfoAttributesResponse: '/v3/products/info/attributes',
        AnalyticsDataResponse: '/v1/analytics/data',
        PostingFBOListResponse: '/v2/posting/fbo/list',
        PostingFBSListResponse: 'v3/posting/fbs/list',
        ProductInfoDiscountedResponse: '/v1/product/info/discounted'
    }

    def __init__(self, engine: OzonAsyncEngine):
        self._engine = engine

    def get_api(self, response_type: Type[BaseResponse]):
        url = OzonAPIFactory.api_list.get(response_type)
        api = OzonAsyncApi(self._engine, url, response_type)

        return api


class OzonPerformanceAPIFactory:
    """Фабрика для endpoint'ов апи. Получение инстанса апи для каждого типа возвращаемого значения."""

    api_list: dict[Type[BaseResponse], str] = {
        ClientCampaignResponse: '/api/client/campaign',
        ClientStatisticsDailyJSONResponse: '/api/client/statistics/daily/json',
        ClientStatisticsJSONResponse: '/api/client/statistics/json',
        ClientStatisticsUUIDResponse: '/api/client/statistics/{UUID}',
        ClientStatisticsReportResponse: '/api/client/statistics/report',
        ClientCampaignObjectsResponse: '/api/client/campaign/{campaignId}/objects',
        ClientCampaignSearchPromoProductsResponse: '/api/client/campaign/{campaignId}/search_promo/products',
    }

    def __init__(self, engine: OzonPerformanceAsyncEngine):
        self._engine = engine

    def get_api(self, response_type: Type[BaseResponse]):
        url = OzonPerformanceAPIFactory.api_list.get(response_type)
        api = OzonAsyncApi(self._engine, url, response_type)

        return api
