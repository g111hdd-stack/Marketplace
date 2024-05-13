from typing import Type

from .response import *
from .response import BaseResponse
from .wb_async_api import WBAsyncApi
from .core import WBAsyncEngine


class WBAPIFactory:

    api_list: dict[Type[BaseResponse], str] = {
        SupplierSalesResponse: 'https://statistics-api.wildberries.ru/api/v1/supplier/sales',
        PromotionAdvertsResponse: 'https://advert-api.wb.ru/adv/v1/promotion/adverts',
        FullstatsResponse: 'https://advert-api.wb.ru/adv/v2/fullstats',
        NMReportDetailResponse: 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/detail',
        ListGoodsFilterResponse: 'https://discounts-prices-api.wb.ru/api/v2/list/goods/filter'
    }

    def __init__(self, engine: WBAsyncEngine):
        self._engine = engine

    def get_api(self, response_type: Type[BaseResponse]):
        url = WBAPIFactory.api_list.get(response_type)
        api = WBAsyncApi(self._engine, url, response_type)
        return api
