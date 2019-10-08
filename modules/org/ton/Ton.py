import base64

import aiohttp

import asyncio

from typing import Dict


# kQD8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYHa6


class Ton:
    def __init__(self, session: aiohttp.ClientSession = None) -> None:
        self.limit: int = 0
        self.limit_max: int = 30
        self.session: aiohttp.ClientSession = session
        self.api_link: str = "https://api.ton.sh/"
        self.ton_test: str = "https://toncenter.com/api/test/v1"

    async def getAdressInformation(self, address: str):
        if self.limit == self.limit_max:
            await asyncio.sleep(60)
            self.limit = 0
        async with self.session.get(url=f"{self.api_link}+getAdressInformation?address={address}") as response:
            print(response)

    async def getaccountforms(self, address: str):
        base: str = base64.urlsafe_b64encode(address.encode(encoding="UTF-8"))
        base = str(base).replace("b'", "").replace("'","")
        async with self.session.post(url=self.ton_test,
                                     json={"jsonrpc": "2.0", "id": 1, "method": "getaccountforms",
                                           "params": ["-1:8156775b79325e5d62e742d9b96c30b6515a5cd2f1f64c5da4b193c03f070e0d"]}, headers={'Content-Type': 'application/json'}) as response:
            print({"jsonrpc": "2.0", "id": 1, "method": "getaccountforms",
                   "params": [f"-1:{base}"]})
            print(await response.json())


async def n():
    async with aiohttp.ClientSession() as session:
        d = Ton(session=session)
        await d.getaccountforms(address="kQD8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYHa6")


asyncio.run(n())
