import asyncio
import aiohttp
import logging

logger = logging.getLogger(__name__)


class WBAsyncEngine:
    def __init__(self, api_key: str = ''):
        self.__headers = {
            'Authorization': api_key
        }

    async def get(self, url: str, params: dict) -> dict:
        response = await self._perform_get_request(url, params)
        return response

    async def post(self, url: str, json: dict, params: dict) -> dict:
        response = await self._perform_post_request(url, json, params)
        return response

    async def _perform_get_request(self, url, params, retry: int = 6):
        async with await self._get_session() as session:
            while retry != 0:
                new_params = {k: v for k, v in params.items() if v is not None}
                async with session.get(url, params=new_params) as response:
                    logger.info(f"Получен ответ от {url} ({response.status})")
                    if response.status in [429, 502]:
                        logger.error(f"Попытка повторного запроса. Осталось попыток: {retry - 1}")
                        await asyncio.sleep(60)
                        retry -= 1
                        continue
                    return await response.json(content_type=None)
            raise Exception

    async def _perform_post_request(self, url, json=None, params=None, retry: int = 6):
        async with await self._get_session() as session:
            while retry != 0:
                async with session.post(url, json=json, params=params) as response:
                    logger.info(f"Получен ответ от {url} ({response.status})")
                    if response.status in [429, 502]:
                        logger.error(f"Попытка повторного запроса. Осталось попыток: {retry - 1}")
                        await asyncio.sleep(60)
                        retry -= 1
                        continue
                    return await response.json()
            raise Exception

    async def _get_session(self):
        session = aiohttp.ClientSession()

        session.headers["Authorization"] = self.__headers['Authorization']
        session.headers["Accept"] = 'application/json'

        return session
