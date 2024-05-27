from typing import Type, Union

from .core import OzonAsyncEngine, OzonPerformanceAsyncEngine
from .response import BaseResponse


class OzonAsyncApi:

    def __init__(self, engine: Union[OzonAsyncEngine, OzonPerformanceAsyncEngine], url: str,
                 response_type: Type[BaseResponse]):
        self._engine = engine
        self._url = url
        self._response_type = response_type

    async def get(self, request, path: str = None):
        parameters = request.dict(by_alias=True)
        url = self._url
        if path is not None:
            url += f'/{path}'
        response = await self._engine.get(url, parameters)
        data = await self._parse_response(response)
        return data

    async def post(self, request):
        parameters = request.dict(by_alias=True)
        response = await self._engine.post(self._url, parameters)
        data = await self._parse_response(response)
        return data

    async def _parse_response(self, response: dict or list):
        if all(key.isdigit() for key in response.keys()):
            new_response = {'result': []}
            for k, v in response.items():
                new_response['result'].append({'id': k, 'statistic': v})
            data = await self._parse_response_object(new_response)
        else:
            data = await self._parse_response_object(response)
        return data

    async def _parse_response_object(self, response: dict):
        if response.get("error"):
            raise Exception(response.get("errorText"))
        return self._response_type.parse_obj(response)
