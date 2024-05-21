from .core import YandexAsyncEngine
from typing import Type
from .response import BaseResponse


class YandexAsyncApi:

    def __init__(self, engine: YandexAsyncEngine, url: str, response_type: Type[BaseResponse]):
        self._engine = engine
        self._url = url
        self._response_type = response_type

    async def get(self, request):
        parameters = request.dict(by_alias=True)
        response = await self._engine.get(self._url, parameters)
        data = await self._parse_response(response)
        return data

    async def post(self, body=None, query=None):
        if body:
            body = await self.params_to_dict(body)
        if query:
            query = await self.params_to_dict(query)
        response = await self._engine.post(self._url, json=body, params=query)
        data = await self._parse_response(response)
        return data

    @staticmethod
    async def params_to_dict(params: list or dict) -> list or dict:
        if isinstance(params, list):
            parameters = [param.dict(by_alias=True) for param in params]
        else:
            parameters = params.dict(by_alias=True)
        return parameters

    async def _parse_response(self, response: dict or list):
        if response.get("error"):
            raise Exception(response.get("errorText"))

        data = await self._parse_response_object(response)
        return data

    async def _parse_response_object(self, response: dict):
        if response.get("error"):
            raise Exception(response.get("errorText"))
        return self._response_type.parse_obj(response)
