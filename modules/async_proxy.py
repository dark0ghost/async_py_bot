import aiohttp
import re

from aiohttp_socks import SocksConnector
from bs4 import BeautifulSoup
from typing import List, Tuple, Iterator, Any, Optional


class Proxy:
    cache_list: List[str]

    def __init__(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        """

        @param session:
        """
        self.session = session

    async def request(self, session: aiohttp.ClientSession, url: str) -> str:
        """

        @param session:
        @param url:
        @return:
        """
        async with session.get(url) as response:
            return await response.text()

    async def pars(self, obj) -> Iterator[Tuple[Any, str]]:
        """

        @param obj:
        @return:
        """
        soup = BeautifulSoup(obj, 'html.parser')
        res = str(soup.table)
        lis = [2, 9, 16, 23, 30, 37, 44, 51, 58, 65, 72, 79, 86, 93, 100, 107, 114, 121, 128, 135, 142, 149, 156, 163]
        ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", res)
        td = soup.find('table').find_all('td')
        a = []
        for li in lis:
            tds = td[li:li + 2]
            port = str(tds[1].find_all('script'))
            port = port[53:60].replace("')", "").replace("<", "")
            a.append(port)
        return zip(ip, a)

    async def main(self) -> List[str]:
        """

        @return:
        """
        links = ["http://www.gatherproxy.com/ru/sockslist"]
        listproxy = []
        for link in links:
            html = await self.request(self.session, link)
            socks5 = await self.pars(html)
            for i in socks5:
                proxy = f"socks5://{i[0]}:{i[1]}"
                listproxy.append(proxy)
            self.cache_list = listproxy
        return listproxy

    async def open_session(self, proxy: str = None) -> aiohttp.ClientSession:
        """

        @param proxy:
        @return:
        """
        if proxy is None:
            self.session = aiohttp.ClientSession()
            return self.session
        connector = SocksConnector.from_url(proxy)
        self.session = aiohttp.ClientSession(connector=connector)
        return self.session

    async def close(self) -> None:
        """

        @return:
        """
        await self.session.close()
        return
