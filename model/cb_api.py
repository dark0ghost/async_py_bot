import aiohttp

from typing import Dict


class CenterBankApi:
    def __init__(self, session: aiohttp.ClientSession):
        self.link = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.obj = dict()
        self.date: str = ""
        self.session: aiohttp.ClientSession = session

    async def GetJson(self) -> Dict:
            async with self.session.get(self.link) as response:
                return await response.json(content_type=None, encoding="utf-8")

    async def Bild(self):
        response = await self.GetJson()
        self.date: str = response['Date']
        for i in response["Valute"].items():
            self.obj[i[0]] = {
                "name": i[1]["Name"],
                "valvue": i[1]["Value"]
            }
        return self.obj

    def __len__(self) -> int:
        return len(self.obj)
