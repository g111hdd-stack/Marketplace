from .requests import *
from .response import *
from .core import SberAsyncEngine
from .sb_endpoints_list import SberAPIFactory


class SberApi:

    def __init__(self, client_id: str, api_key: str):
        self._engine = SberAsyncEngine()
        self._api_factory = SberAPIFactory(self._engine)
        self._client_id = client_id
        self._api_key = api_key

        self._order_service_order_get_api = self._api_factory.get_api(OrderServiceOrderGetResponse)
        self._order_service_order_search_api = self._api_factory.get_api(OrderServiceOrderSearchResponse)

    async def get_order_service_order_search(self, date_from: str, date_to: str, statuses: list[str],
                                             count: int = 1000) -> OrderServiceOrderSearchResponse:
        request = OrderServiceOrderSearchRequest(data=OrderServiceOrderSearchDataRequest(token=self._api_key,
                                                                                         dateFrom=date_from,
                                                                                         dateTo=date_to,
                                                                                         count=count,
                                                                                         statuses=statuses))
        answer: OrderServiceOrderSearchResponse = await self._order_service_order_search_api.post(request)
        return answer

    async def get_order_service_orders(self, shipments: list[str]) -> OrderServiceOrderGetResponse:
        request = OrderServiceOrderGetRequest(data=OrderServiceOrderGetDataRequest(token=self._api_key,
                                                                                   shipments=shipments,
                                                                                   merchantId=self._client_id))
        answer: OrderServiceOrderGetResponse = await self._order_service_order_get_api.post(request)

        return answer
