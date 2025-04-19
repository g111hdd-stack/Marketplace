import asyncio
import aiohttp
import logging

logger = logging.getLogger(__name__)


async def transform_params(params) -> dict:
    new_params = {k: v for k, v in params.items() if v is not None}
    for k, v in new_params.items():
        if isinstance(v, bool):
            new_params[k] = str(v)
    return new_params


class YandexAsyncEngine:
    def __init__(self, api_key: str = ''):
        self._base_url = 'https://api.partner.market.yandex.ru'
        self.__headers = {
            'Authorization': api_key,
            'Api-Key': api_key
        }

    async def get(self, url: str, params: dict) -> dict:
        url = await self._get_url(url)
        response = await self._perform_get_request(url, params)

        return response

    async def post(self, url: str, json: dict, params: dict) -> dict:
        url = await self._get_url(url)
        response = await self._perform_post_request(url, json, params)

        return response

    async def _get_url(self, url: str):
        if url.startswith("/"):
            return self._base_url + url
        else:
            return f"{self._base_url}/{url}"

    async def _perform_get_request(self, url, params, retry: int = 6):
        async with await self._get_session() as session:
            while retry != 0:
                try:
                    params = await transform_params(params)
                    async with session.get(url, params=params) as response:
                        if response.status != 200:
                            logger.info(f"Получен ответ от {url} ({response.status})")
                            logger.error(f"Попытка повторного запроса. Осталось попыток: {retry - 1}")
                            await asyncio.sleep(60)
                            retry -= 1
                            continue
                        return await response.json(content_type=None)
                except (aiohttp.ClientConnectionError, aiohttp.ClientError, asyncio.TimeoutError) as e:
                    logger.error(f"Ошибка соединения: {e}")
                    logger.error(f"Попытка повторного запроса. Осталось попыток: {retry - 1}")
                    await asyncio.sleep(60)
                    retry -= 1
                    continue
            raise Exception

    async def _perform_post_request(self, url, json=None, params=None, retry: int = 6):
        async with await self._get_session() as session:
            while retry != 0:
                try:
                    if json is not None:
                        json = await transform_params(json)
                    if params is not None:
                        params = await transform_params(params)
                    async with session.post(url, json=json, params=params) as response:
                        if response.status != 200:
                            logger.info(f"Получен ответ от {url} ({response.status})")
                            logger.error(f"Попытка повторного запроса. Осталось попыток: {retry - 1}")
                            await asyncio.sleep(60)
                            retry -= 1
                            continue
                        return await response.json()
                except (aiohttp.ClientConnectionError, aiohttp.ClientError, asyncio.TimeoutError) as e:
                    logger.error(f"Ошибка соединения: {e}")
                    logger.error(f"Попытка повторного запроса. Осталось попыток: {retry - 1}")
                    await asyncio.sleep(60)
                    retry -= 1
                    continue
            raise Exception

    async def _get_session(self):
        session = aiohttp.ClientSession()

        session.headers["Authorization"] = 'Bearer ' + self.__headers['Authorization']
        session.headers["Api-Key"] = self.__headers['Api-Key']

        return session
