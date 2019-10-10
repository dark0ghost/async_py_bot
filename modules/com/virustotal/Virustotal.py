import aiofiles
import aiohttp

from typing import Dict

import asyncio


class Virustotal:
    """
    this class use api virustotal.com
    ues:
     async def start():
       d = Virustotal()
       await d.new_session()
       async with aiofiles.open("db_pg.py") as reponse:
        print(await d.file_scan(name_file="db_pg.py", file=reponse))
       await d.close()

     asyncio.run(start())
    """

    def __init__(self, api_key: str, session: aiohttp.ClientSession = None, is_public: bool = True) -> None:
        """

        :param api_key:
        :param session:
        """
        self.session = session
        self.api_key: str = api_key
        self.api_link: str = "https://www.virustotal.com/vtapi/v2/"
        self.is_public = is_public
        if is_public:
            self.limit: int = 0
            self.limit_max: int = 4

    async def new_session(self) -> aiohttp.ClientSession:
        """

        :return:
        """
        self.session = aiohttp.ClientSession()
        return self.session

    async def close(self) -> aiohttp.ClientSession.close:
        """

        :return:
        """
        return await self.session.close()

    async def file_report(self, resource: str, allinfo: bool = False) -> Dict[str, str]:
        """

        :param resource:
        :param allinfo:
        :return:
        """
        if self.is_public and self.limit == self.limit_max:
            await asyncio.sleep(60)
            self.limit: int = 0
        self.limit += 1
        async with self.session.get(
                url=f"{self.api_link}file/report?apikey={self.api_key}&resource={resource}&allinfo={str(allinfo).lower()}") as response:
            return await response.json()

    async def file_scan(self, name_file: str, file: aiofiles.open) -> Dict[str, str]:
        """

        :param name_file:
        :param file:
        :return:
        """
        if self.is_public and self.limit == self.limit_max:
            await asyncio.sleep(60)
            self.limit: int = 0
        self.limit += 1
        async with self.session.post(url=f"{self.api_link}file/scan", data={'file': (name_file, file)},
                                     params={"apikey": self.api_key,
                                             "Content-Type": "text/json; charset=utf-8"}) as response:
            return await response.json()

    async def file_scan_upload_url(self, name_file: str, file: aiofiles.open) -> Dict[str, str]:
        if not self.is_public:
            async with self.session.get(url=f"{self.api_link}file/scan/upload_url",
                                        params={"apikey": self.api_key,
                                                "Content-Type": "text/json; charset=utf-8"}) as response:
                dict_response: Dict[str, str] = await response.json()
                url_response: str = dict_response['upload_url']

                files = {'file': (name_file, file)}
                async with self.session.post(url=url_response, json=files) as rep:
                    return await rep.json()

        raise RuntimeError("is private api https://developers.virustotal.com/reference#file-scan-upload-url")

    async def file_rescan(self, link: str):
        if self.is_public and self.limit == self.limit_max:
            await asyncio.sleep(60)
            self.limit: int = 0
        self.limit += 1
        params = {'apikey': self.api_key, 'resource': link}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with self.session.post(url=f"{self.api_link}file/rescan", params=params, headers=headers) as response:
            return await response.json()

    async def file_download(self, hash: str):
        if self.is_public and self.limit == self.limit_max:
            await asyncio.sleep(60)
            self.limit: int = 0
        self.limit += 1
        params = {'apikey': self.api_key, 'hash': hash}
        async with self.session.get(url=f"{self.api_link}file/download", params=params) as response:
            return await response.json()





