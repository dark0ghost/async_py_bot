import aiohttp
import asyncio

from typing import Dict


class School:
    def __init__(self, token: str, session: aiohttp.ClientSession, proxy_link: str = None,
                 proxy_auth: aiohttp.BasicAuth = None) -> None:
        self.session = session
        self.api_link: str = "https://api.dnevnik.ru/v2/"
        self.api_token: str = token
        self.headers: Dict[str, str] = {
            "token": self.api_token,
        }

    async def get_user(self, id_user: int):
        pass

    async def proxy_sesseion(self):
        pass

    async def authorizations(self):
        async with self.session.post(self.api_link + "/authorizations") as response:
            print(await response.json())


async def o():
    s = aiohttp.ClientSession()
    # print(await async_proxy.main(s))
    f = School(token="kasjdh", session=s)
    await f.authorizations()
    await s.close()


asyncio.run(o())
