import aiohttp
import typing
from bs4 import BeautifulSoup

import asyncio

from aiohttp_socks import SocksConnector


class Podcasts:
    def __init__(self, session: typing.Optional[aiohttp.ClientSession] = None):
        """

        """
        self.session = session
        self.api: str = ""

    async def open_session(self, proxy: typing.Optional[str] = None) -> aiohttp.ClientSession:
        if proxy is None:
            self.session = aiohttp.ClientSession()
            return self.session
        connector = SocksConnector.from_url(proxy)
        self.session = aiohttp.ClientSession(connector=connector)
        return self.session

    async def close(self) -> None:
        await self.session.close()
        return

    async def forismatic(self) -> typing.Dict[str, str]:
        forist: str = "https://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=json&lang=ru"
        async with self.session.get(url=forist) as response:
            return await response.json()

    async def mk_andekdoit(self):
        mk_api: str = "https://www.mk.ru/anekdoti/"
        async with self.session.get(url=mk_api) as response:
            text = await response.text()



