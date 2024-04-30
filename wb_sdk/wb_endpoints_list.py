from typing import Type

from .response import SupplierSalesResponse
from .response import BaseResponse
from .wb_async_api import WBAsyncApi
from .core import WBAsyncEngine


class WBAPIFactory:

    api_list: dict[Type[BaseResponse], str] = {
        SupplierSalesResponse: 'https://statistics-api.wildberries.ru/api/v1/supplier/sales'
    }

    def __init__(self, engine: WBAsyncEngine):
        self._engine = engine

    def get_api(self, response_type: Type[BaseResponse]):
        url = WBAPIFactory.api_list.get(response_type)
        api = WBAsyncApi(self._engine, url, response_type)
        return api
