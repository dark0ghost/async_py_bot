
import aiohttp


class CatApi:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session: aiohttp.ClientSession = session

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
    f = CatApi(session=s)
    print(await f.get_photo())
    await s.close()


asyncio.run(start())
"""

