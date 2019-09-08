import aiohttp
import re
from bs4 import BeautifulSoup


async def request(session, url):
    async with session.get(url) as response:
        return await response.text()


async def pars(obj):
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


async def main(session: aiohttp.ClientSession):
    links = ["http://www.gatherproxy.com/ru/sockslist", ]
    listproxy = []
    for link in links:
        html = await request(session, link)
        socks5 = await pars(html)
        for i in socks5:
            proxy = f"socks5://{i[0]}:{i[1]}"
            listproxy.append(proxy)

    return listproxy
