import aiohttp
import asyncio


from typing import Dict

from aiohttp_socks import SocksConnector


class Ton:
    """
    this class use api  https://api.ton.sh/ and  https://toncenter.com/api/test/v1 and will use ton.org api
    use:
    async def n():
      async with aiohttp.ClientSession() as session:
        d = Ton(session=session)
        print(await d.getAddressInformation(addres=kQD8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYHa6) #addres this you wallet )
        #{"ok":true,"result":{"state":"active","balance":19869804595}}

        #use proxy
         await d.proxy_session(proxy_url="socks5://3833844140:w61D1u0v@orbtl.s5.opennetwork.cc:999")
         # code
         await d.close()

    asyncio.run(n())

    """

    def __init__(self, session: aiohttp.ClientSession = None) -> None:
        """

        :param session:
        """
        self.limit: int = 0
        self.limit_max: int = 30
        self.session: aiohttp.ClientSession = session
        self.api_link: str = "https://api.ton.sh/"
        self.ton_test: str = "https://toncenter.com/api/test/v1"

    async def getAddressInformation(self, address: str) -> Dict[str, str]:
        """

        :param address:
        :return:
        """
        if self.limit == self.limit_max:
            await asyncio.sleep(60)
            self.limit = 0
        self.limit += 1
        async with self.session.get(url=f"{self.api_link}getAddressInformation?address={address}") as response:
            return await response.json()

    async def get_account_forms(self, address: str) -> Dict[str, str]:
        """

        :param address:
        :return:
        """
        async with self.session.post(url=self.ton_test,
                                     json={"jsonrpc": "2.0", "id": 1, "method": "getaccountforms",
                                           "params": [address]},
                                     headers={'Content-Type': 'application/json'}) as response:
            return await response.json()

    async def getAddressBalance(self, address: str) -> int:
        """

        :param address:
        :return:
        """
        if self.limit == self.limit_max:
            await asyncio.sleep(60)
            self.limit = 0
        self.limit += 1
        async with self.session.get(url=f"{self.api_link}getAddressBalance?address={address}") as response:
            return (await response.json())["result"]

    async def getAddressState(self, address: str) -> str:
        if self.limit == self.limit_max:
            await asyncio.sleep(60)
            self.limit = 0
        self.limit += 1
        async with self.session.get(url=f"{self.api_link}getAddressState?address={address}") as response:
            return (await response.json())["result"]

    async def convertAddressToRaw(self, address: str) -> str:
        """

        :param address:
        :return:
        """
        if self.limit == self.limit_max:
            await asyncio.sleep(60)
            self.limit = 0
        self.limit += 1
        async with self.session.get(url=f"{self.api_link}convertAddressToRaw?address={address}") as response:
            return (await response.json())["result"]

    async def time_server(self) -> str:
        """

        :return:
        """
        async with self.session.post(url=self.ton_test,
                                     json={"jsonrpc": "2.0", "id": 1, "method": "time", "params": []}) as response:
            return (await response.json())["result"]

    async def getblock(self, block: str) -> Dict[str, str]:
        """

        :param block:
        :return:
        """
        async with self.session.post(url=self.ton_test, json={"jsonrpc": "2.0", "id": 1, "method": "getblock",
                                                              "params": [block]}) as response:
            return await response.json()

    async def shardsinfo(self) -> Dict[str, str]:
        """

        :return:
        """
        async with self.session.post(url=self.ton_test, json={"jsonrpc": "2.0", "id": 1, "method": "shardsinfo",
                                                              "params": []}) as response:
            return await response.json()

    async def getaccount(self, address: str) -> Dict[str, str]:
        """

        :param address:
        :return:
        """
        async with self.session.post(url=self.ton_test, json={"jsonrpc": "2.0", "id": 1, "method": "getaccount",
                                                              "params": [address]}) as response:
            return await response.json()

    async def sendboc(self, address: str) -> Dict[str, str]:
        """

        :param address:
        :return:
        """
        async with self.session.post(url=self.ton_test, json={"jsonrpc": "2.0", "id": 1, "method": "sendboc",
                                                              "params": [address]}) as response:
            return await response.json()

    def create_wallet(self):
        """
        todo : wait api full
        :return:
        """

    def create_key_gen(self):
        """
                todo : wait api full
                :return:
        """

    async def proxy_session(self, proxy_url: str) -> aiohttp.ClientSession:
        """
         proxy_url ="socks5://user:password@127.0.0.1:1080" or "socks5://127.0.0.1:1080"
        :param proxy_url:
        :return:
        """
        connector = SocksConnector.from_url(proxy_url)
        self.session = aiohttp.ClientSession(connector=connector)
        return self.session

    async def close(self) -> bool:
        """

        :return:
        """
        await self.session.close()
        return True

