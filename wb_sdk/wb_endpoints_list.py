from typing import Type

from .response import *
from .response import BaseResponse
from .wb_async_api import WBAsyncApi
from .core import WBAsyncEngine


class WBAPIFactory:

    api_list: dict[Type[BaseResponse], str] = {
        SupplierSalesResponse: 'https://statistics-api.wildberries.ru/api/v1/supplier/sales',
        PromotionAdvertsResponse: 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts',
        FullstatsResponse: 'https://advert-api.wildberries.ru/adv/v2/fullstats',
        NMReportDetailResponse: 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/detail',
        ListGoodsFilterResponse: 'https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter',
        SupplierReportDetailByPeriodResponse: 'https://statistics-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod',
        PaidStorageResponse: 'https://seller-analytics-api.wildberries.ru/api/v1/paid_storage',
        PaidStorageStatusResponse: 'https://seller-analytics-api.wildberries.ru/api/v1/paid_storage/tasks/{task_id}/status',
        PaidStorageDownloadResponse: 'https://seller-analytics-api.wildberries.ru/api/v1/paid_storage/tasks/{task_id}/download',
        SupplierOrdersResponse: 'https://statistics-api.wildberries.ru/api/v1/supplier/orders',
        AnalyticsAcceptanceReportResponse: 'https://seller-analytics-api.wildberries.ru/api/v1/analytics/acceptance-report',
        AnalyticsAntifraudDetailsResponse: 'https://seller-analytics-api.wildberries.ru/api/v1/analytics/antifraud-details',
        NmReportDownloadsResponse: 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads',
        NmReportDownloadsFileResponse: 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/downloads/file/{downloadId}',
        WarehouseRemainsResponse: 'https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains',
        WarehouseRemainsTasksStatusResponse: 'https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains/tasks/{task_id}/status',
        WarehouseRemainsTasksDownloadResponse: 'https://seller-analytics-api.wildberries.ru/api/v1/warehouse_remains/tasks/{task_id}/download',
        SupplierStocksResponse: 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
    }

    def __init__(self, engine: WBAsyncEngine):
        self._engine = engine

    def get_api(self, response_type: Type[BaseResponse]):
        url = WBAPIFactory.api_list.get(response_type)
        api = WBAsyncApi(self._engine, url, response_type)
        return api
