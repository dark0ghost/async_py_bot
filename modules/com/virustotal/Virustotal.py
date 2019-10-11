from datetime import datetime

import aiofiles
import aiohttp

from typing import Dict, Optional

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

    def is_limit(self) -> bool:
        """

        :return:
        """
        return self.is_public and self.limit == self.limit_max

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
        if self.is_limit():
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
        if self.is_limit():
            await asyncio.sleep(60)
            self.limit: int = 0
        self.limit += 1
        async with self.session.post(url=f"{self.api_link}file/scan", data={'file': (name_file, file)},
                                     params={"apikey": self.api_key,
                                             "Content-Type": "text/json; charset=utf-8"}) as response:
            return await response.json()

    async def file_scan_upload_url(self, name_file: str, file: aiofiles.open) -> Dict[str, str]:
        """

        :param name_file:
        :param file:
        :return:
        """
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

    async def file_rescan(self, link: str) -> Dict[str, str]:
        """

        :param link:
        :return:
        """
        if self.is_limit():
            await asyncio.sleep(60)
            self.limit: int = 0
        self.limit += 1
        params = {'apikey': self.api_key, 'resource': link}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with self.session.post(url=f"{self.api_link}file/rescan", params=params, headers=headers) as response:
            return await response.json()

    async def file_download(self, hash_file: str) -> Dict[str, str]:
        """
        :param hash_file:
        :return:
        """
        if not self.is_public:
            params = {'apikey': self.api_key, 'hash': hash_file}
            async with self.session.get(url=f"{self.api_link}file/download", params=params) as response:
                return await response.json()
        raise RuntimeError("is private api https://developers.virustotal.com/reference#file-download")

    async def file_behaviour(self, hash_files: str) -> Dict[str, str]:
        """

        :param hash_files:
        :return:
        """
        if not self.is_public:
            params = {'apikey': self.api_key, 'hash': hash_files}
            async with self.session.get(url=f"{self.api_link}file/behaviour", params=params) as response:
                return await response.json()
        raise RuntimeError("is private api https://developers.virustotal.com/reference#file-behaviour")

    async def file_network_traffic(self, hash_file) -> Dict[str, str]:
        """

        :param hash_file:
        :return:
        """
        if not self.is_public:
            params = {'apikey': self.api_key, 'hash': hash_file}
            async with self.session.get(url=f"{self.api_link}file/network-traffic", params=params) as response:
                return await response.json()
        raise RuntimeError("is private api https://developers.virustotal.com/reference#file-network-traffic")

    async def file_feed(self, package: str) -> bytes:
        """

        :param package:
        :return:
        """
        if not self.is_public:
            params = {'apikey': self.api_key, 'package': package}
            async with self.session.get(url=f"{self.api_link}file/feed", params=params, stream=True,
                                        allow_redirects=True) as response:
                async with aiofiles.open('package.tar.bz2', 'wb') as file:
                    await file.write(await response.read())
                    return await response.read()
        raise RuntimeError("is private api https://developers.virustotal.com/reference#file-feed")

    async def file_clusters(self, date: datetime) -> Dict[str, str]:
        """

        :param date:
        :return:
        """
        if not self.is_public:
            params = {'apikey': self.api_key, 'date': date}
            async with self.session.get(url=f"{self.api_link}file/clusters", params=params) as response:
                return await response.json()
        raise RuntimeError("is private api https://developers.virustotal.com/reference#file-clusters")

    async def file_search(self, query: str) -> Dict[str, str]:
        """

        :param query:
        :return:
        """
        if not self.is_public:
            params = {'apikey': self.api_key, 'query': query}
            async with self.session.get(url=f"{self.api_link}file/search", params=params) as response:
                return await response.json()
        raise RuntimeError("is private api https://developers.virustotal.com/reference#file-search")

    async def url_report(self, resource: str, allinfo: bool = False, scan: int = 0) -> Dict[str, str]:
        """

        :param resource:
        :param allinfo:
        :param scan:
        :return:
        """
        if self.is_limit():
            await asyncio.sleep(60)
            self.limit: int = 0
        self.limit += 1
        params = {'apikey': self.api_key, 'resourse': resource, "allinfo": str(allinfo).lower(), "scan": scan}
        async with self.session.get(url=f"{self.api_link}url/report", params=params) as response:
            return await response.json()

    async def url_feed(self) -> None:
        """
        not aio version
        :return:
        """
        raise RuntimeError("is private api https://developers.virustotal.com/reference#file-feed")

    async def domain_report(self, domain: str) -> Dict[str, str]:
        """

        :param domain:
        :return:
        """
        if self.is_limit():
            await asyncio.sleep(60)
            self.limit: int = 0
        self.limit += 1
        params = {'apikey': self.api_key, 'domain': domain}
        async with self.session.get(url=f"{self.api_link}domain/report", params=params) as response:
            return await response.json()

    async def ip_address_report(self, ip: str) -> Dict[str, str]:
        """

        :param ip:
        :return:
        """
        if self.is_limit():
            await asyncio.sleep(60)
            self.limit: int = 0
        self.limit += 1
        params = {'apikey': self.api_key, 'ip': ip}
        async with self.session.get(url=f"{self.api_link}ip-address/report", params=params) as response:
            return await response.json()

    async def comments_get(self, resource: str, before: Optional[datetime] = None) -> Dict[str, str]:
        """

        :param resource:
        :param before:
        :return:
        """
        if self.is_limit():
            await asyncio.sleep(60)
            self.limit: int = 0
        self.limit += 1
        if before is None:
            params = {'apikey': self.api_key, 'resource': resource}
        else:
            params = {'apikey': self.api_key, 'resource': resource, "before": before}

        async with self.session.get(url=f"{self.api_link}comments/get", params=params) as response:
            return await response.json()

    async def comments_put(self, resource: str, comments: str):
        """

        :param resource:
        :param comments:
        :return:
        """
        if self.is_limit():
            await asyncio.sleep(60)
            self.limit: int = 0
        self.limit += 1
        params = {'apikey': self.api_key, 'resource': resource, "comments": comments}
        async with self.session.post(url=f"{self.api_link}comments/put", params=params) as response:
            return await response.json()
