import json
from aiohttp import ClientSession
from app import logger
from config import CONFIG

class RESITA_API:
    def __init__(self):
        self.api_url = "https://api.ferdev.my.id"
        self.api_key = CONFIG.RESITA_API_KEY

    async def sendGetReq(self, path, params):
        """
        :param path: api execution path
        :param params: param that required for the path (except apikey)
        """
        try:
            params["apikey"] = self.api_key

            async with ClientSession() as session:
                async with session.get(f"{self.api_url}{path}", params=params) as response:
                    res = await response.text()
                    return json.loads(res)
        except Exception as e:
            logger.error(e)
            return str(e)
