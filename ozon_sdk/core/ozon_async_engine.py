import asyncio
import aiohttp
import logging

logger = logging.getLogger(__name__)


class OzonAsyncEngine:

    def __init__(self, client_id: str = '', api_key: str = ''):
        self._base_url = 'https://api-seller.ozon.ru'
        self.__headers = {
            'Client-Id': client_id,
            'Api-Key': api_key
        }

    async def get(self, url: str, params: dict) -> dict:
        url = await self._get_url(url)
        response = await self._perform_get_request(url, params)
        return response

    async def post(self, url: str, params: dict) -> dict:
        url = await self._get_url(url)
        response = await self._perform_post_request(url, params)
        return response

    async def _get_url(self, url: str):
        if url.startswith("/"):
            return self._base_url + url
        else:
            return f"{self._base_url}/{url}"

    async def _perform_get_request(self, url, params, retry: int = 6):
        async with await self._get_session() as session:
            while retry != 0:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        logger.info(f"Получен ответ от {url} ({response.status})")
                        logger.error(f"Попытка повторного запроса. Осталось попыток: {retry - 1}")
                        await asyncio.sleep(60)
                        retry -= 1
                        continue
                    return await response.json(content_type=None)
            raise Exception

    async def _perform_post_request(self, url, params, retry: int = 6):
        async with await self._get_session() as session:
            while retry != 0:
                async with session.post(url, json=params) as response:
                    if response.status != 200:
                        logger.info(f"Получен ответ от {url} ({response.status})")
                        logger.error(f"Попытка повторного запроса. Осталось попыток: {retry - 1}")
                        await asyncio.sleep(60)
                        retry -= 1
                        continue
                    return await response.json()
            raise Exception

    async def _get_session(self):
        session = aiohttp.ClientSession()

        session.headers["Client-Id"] = self.__headers['Client-Id']
        session.headers["Api-Key"] = self.__headers['Api-Key']

        return session
