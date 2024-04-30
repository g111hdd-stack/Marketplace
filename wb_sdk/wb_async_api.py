from typing import Type

from .core import WBAsyncEngine
from .response import BaseResponse


class WBAsyncApi:

    def __init__(self, engine: WBAsyncEngine, url: str, response_type: Type[BaseResponse]):
        self._engine = engine
        self._url = url
        self._response_type = response_type

    async def get(self, request):
        parameters = request.dict(by_alias=True)
        response = await self._engine.get(self._url, parameters)
        data = await self._parse_response(response)
        return data

    async def post(self, request):
        parameters = request.dict(by_alias=True)
        response = await self._engine.post(self._url, parameters)
        data = await self._parse_response(response)
        return data

    async def _parse_response(self, response: dict or list):
        if isinstance(response, list):
            data = await self._parse_response_object({"result": response})
            return data
        else:
            raise TypeError("This is a TypeError")

    async def _parse_response_object(self, response: dict):
        return self._response_type.parse_obj(response)
