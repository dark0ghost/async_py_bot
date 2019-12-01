import aiohttp
import typing

import asyncio

from aiohttp_socks import SocksConnector


class Etherscan:
    def __init__(self, session: typing.Optional[aiohttp.ClientSession] = None):
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
