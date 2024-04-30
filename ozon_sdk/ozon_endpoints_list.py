from typing import Type

from .response import FinanceTransactionListResponse, PostingFBSGetResponse, PostingFBOGetResponse
from .response import BaseResponse
from .ozon_async_api import OzonAsyncApi
from .core import OzonAsyncEngine


class OzonAPIFactory:
    """Фабрика для endpoint'ов апи. Получение инстанса апи для каждого типа возвращаемого значения."""

    api_list: dict[Type[BaseResponse], str] = {
        FinanceTransactionListResponse: '/v3/finance/transaction/list',
        PostingFBSGetResponse: '/v3/posting/fbs/get',
        PostingFBOGetResponse: '/v2/posting/fbo/get'
    }

    def __init__(self, engine: OzonAsyncEngine):
        self._engine = engine

    def get_api(self, response_type: Type[BaseResponse]):
        url = OzonAPIFactory.api_list.get(response_type)
        api = OzonAsyncApi(self._engine, url, response_type)

        return api
