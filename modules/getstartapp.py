import aiohttp
from aiohttp_socks import SocksConnector


class GetStartApp:
    api = "https://e27.co/api/startups/?tab_name={tab_name}&start={start}&length={length}"

    def __init__(self, session: aiohttp.ClientSession = None, tab_name: str = "recentlyupdated", start: int = 0,
                 length: int = 3060):
        """

        :param session:
        :param tab_name:
        :param start:
        :param length:
        """
        self.api = self.api.format(tab_name=tab_name, start=start, length=length)
        self.session = session

    async def open_session(self, proxy: str = None) -> aiohttp.ClientSession:
        if proxy is None:
            self.session = aiohttp.ClientSession()
            return self.session
        connector = SocksConnector.from_url(proxy)
        self.session = aiohttp.ClientSession(connector=connector)
        return self.session

    async def close(self) -> None:
        await self.session.close()
        return

    async def get_data(self) -> str:
        async with self.session.get(self.api) as response:
            return await response.json()


f = GetStartApp()
