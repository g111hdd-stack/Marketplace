from .core import SberAsyncEngine
from typing import Type
from .response import BaseResponse


class SberAsyncApi:

    def __init__(self, engine: SberAsyncEngine, url: str, response_type: Type[BaseResponse]):
        self._engine = engine
        self._url = url
        self._response_type = response_type

    async def get(self, request):
        parameters = request.dict(by_alias=True)
        response = await self._engine.get(self._url, parameters)
        data = await self._parse_response(response)
        return data

    async def post(self, params):
        params = params.dict(by_alias=True)
        response = await self._engine.post(self._url, params=params)
        data = await self._parse_response(response)
        return data

    async def _parse_response(self, response: dict or list):
        if response.get("error"):
            raise Exception(response.get("errorText"))
        data = await self._parse_response_object(response)
        return data

    async def _parse_response_object(self, response: dict):
        if response.get("error"):
            raise Exception(response.get("errorText"))
        return self._response_type.parse_obj(response)
