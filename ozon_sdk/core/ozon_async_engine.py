import aiohttp


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

    async def _perform_get_request(self, url, params):
        async with await self._get_session() as session:
            async with session.get(url, params=params) as response:
                return await response.json(content_type=None)

    async def _perform_post_request(self, url, params):
        async with await self._get_session() as session:
            async with session.post(url, json=params) as response:
                return await response.json()

    async def _get_session(self):
        session = aiohttp.ClientSession()

        session.headers["Client-Id"] = self.__headers['Client-Id']
        session.headers["Api-Key"] = self.__headers['Api-Key']

        return session
