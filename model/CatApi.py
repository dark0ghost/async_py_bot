from typing import Dict

import aiofiles
import aiohttp


class CatApi:
    def __init__(self, session: aiohttp.ClientSession, token: str = ""):
        self.token: str = token
        self.session: aiohttp.ClientSession = session
        self.api_url: str = "https://api.thecatapi.com/v1/images"
        self.headers: Dict[str, str] = {
            'x-api-key': self.token

        }

    async def auth(self):
        """
        no work
        :return:
        """
        async with self.session.post(url=self.api_url, headers=self.headers, data="1.1.1.1") as response:
            json = await response.json()
            return json["status"] == 200

    async def get_photo(self) -> str:
        async with self.session.get(
                "https://api.thecatapi.com/v1/images/search?limit=5&page=10&order=Desc") as response:
            json = await response.json()
            print(json[1]["url"])
            async with self.session.get(json[0]["url"]) as response_photo:
                with open("./staticfile/cat.jpg", "wb") as f:
                    f.write(await response_photo.read())
                return "/staticfile/cat.jpg"


"""
import asyncio


async def start():
    s = aiohttp.ClientSession()
    f = CatApi(session=s, token="")
    print(await f.get_photo())
    await s.close()


asyncio.run(start())
"""
