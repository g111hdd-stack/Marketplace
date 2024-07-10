from .response import *
from typing import Type
from .ya_async_api import YandexAsyncApi
from .core import YandexAsyncEngine


class YandexAPIFactory:

    api_list: dict[Type[BaseResponse], str] = {
        CampaignsResponse: 'campaigns',
        CampaignsOrdersResponse: 'campaigns/{campaignId}/orders',
        CampaignsStatsOrdersResponse: 'campaigns/{campaignId}/stats/orders',
        ReportsUnitedMarketplaceServicesGenerateResponse: 'reports/united-marketplace-services/generate',
        ReportsInfoResponse: 'reports/info/{reportId}'
    }

    def __init__(self, engine: YandexAsyncEngine):
        self._engine = engine

    def get_api(self, response_type: Type[BaseResponse]):
        url = YandexAPIFactory.api_list.get(response_type)
        api = YandexAsyncApi(self._engine, url, response_type)
        return api
