from asyncio import AbstractEventLoop
from typing import Any, Dict

import aiohttp
import asyncio


class QrTag:
    def __init__(self, session: aiohttp.ClientSession = None) -> None:
        """

        :param session:
        """
        self.api_link: str = "https://qrtag.net/api/"
        self.session: aiohttp.ClientSession = session
        self.sync_data: bytes = None

    async def create(self, data: Any, size: object = 12, form: object = "png", is_sync: bool = False) -> bytes:
        """

        :param is_sync:
        :param data:
        :param size:
        :param form:
        :return:
        """
        async with self.session.get(url=self.api_link + f"qr_{size}.{form}?url={data}") as response:
            if is_sync:
                await self.close()
            return await response.read()

    async def create_session(self) -> aiohttp.ClientSession:
        """

        :return:
        """
        self.session = aiohttp.ClientSession()
        return self.session

    async def close(self) -> None:
        """

        :return:
        """
        await self.session.close()

    async def auto_sync(self, data: Any, size: int = 12, form: str = "png") -> None:
        await self.create_session()
        self.sync_data = await self.create(data=data, size=size, form=form, is_sync=True)

    def sync_call(self, data: Any, size: int = 12, form: str = "png") -> bytes:
        loop: AbstractEventLoop = asyncio.get_event_loop()
        loop.run_until_complete(self.auto_sync(data=data, size=size, form=form))
        return self.sync_data
