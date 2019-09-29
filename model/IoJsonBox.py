import aiohttp

from secrets import token_urlsafe

from typing import Dict, Any


class IOJsonBox:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session: aiohttp.ClientSession = session
        self.api_link: str = "https://jsonbox.io/"
        self.headers: Dict[str, str] = {"content-type": "application/json"}

    async def create_box(self, text: Dict[str, Any]) -> str:
        len_text = len(text)
        if 20 < len_text < 64:
            url = self.api_link + token_urlsafe(len(text))
        else:
            url = self.api_link + (token_urlsafe(29))

        url = url.replace("_", '').replace("-", "")

        async with self.session.post(url=url, headers=self.headers, data=text) as response:
            print(await response.text(), url)
            return url

    async def get_data_link(self, url: str):
        if "https://jsonbox.io/" in url:
            async with self.session.get(url=url) as response:
                return await response.text()
        return "invalid url"