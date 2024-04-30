import aiohttp


class WBAsyncEngine:
    def __init__(self, api_key: str = ''):
        self.__headers = {
            'Authorization': api_key
        }

    async def get(self, url: str, params: dict) -> dict:
        response = await self._perform_get_request(url, params)

        return response

    async def post(self, url: str, params: dict) -> dict:
        response = await self._perform_post_request(url, params)

        return response

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

        session.headers["Authorization"] = self.__headers['Authorization']

        return session
