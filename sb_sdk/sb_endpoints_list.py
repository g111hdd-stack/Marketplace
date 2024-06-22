from .response import *
from typing import Type
from .sb_async_api import SberAsyncApi
from .core import SberAsyncEngine


class SberAPIFactory:

    api_list: dict[Type[BaseResponse], str] = {
        OrderServiceOrderSearchResponse: 'v1/orderService/order/search',
        OrderServiceOrderGetResponse: 'v1/orderService/order/get'
    }

    def __init__(self, engine: SberAsyncEngine):
        self._engine = engine

    def get_api(self, response_type: Type[BaseResponse]):
        url = SberAPIFactory.api_list.get(response_type)
        api = SberAsyncApi(self._engine, url, response_type)
        return api
