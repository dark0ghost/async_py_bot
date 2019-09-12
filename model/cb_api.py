import aiohttp

from typing import Dict


class CenterBankApi:
    """
    class implements api cbr
    """
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.link = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.obj = dict()
        self.date: str = ""
        self.session: aiohttp.ClientSession = session

    async def get_json(self) -> Dict[str, str, str]:
        """
        get json from https://www.cbr-xml-daily.ru/daily_json.js
        :return:
        """
        async with self.session.get(self.link) as response:
            return await response.json(content_type=None, encoding="utf-8")

    async def build_list_coin(self) -> Dict[str, str]:
        """
        build dict from  json
        :return:
        """
        response: Dict[str, str, str] = await self.get_json()
        self.date: str = response['Date']
        for i in response["Valute"].items():
            self.obj[i[0]] = {
                "name": i[1]["Name"],
                "valvue": i[1]["Value"]
            }
        return self.obj

    def __len__(self) -> int:
        """
        return len available coin
        :return:
        """
        return len(self.obj)
