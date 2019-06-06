# This Python file uses the following encoding: utf-8
import asyncio
import json
import logging

import aiohttp
log = logging
log.basicConfig(filename="yandex_api.log")
log.getLogger("api_yandex")


class transport:

    def __init__(self, *args):
        self.transport: dict = {
            "самолет": "plane",
            "поезд": "train",
            "электричка": "suburban",
            "автобус": "bus",
            "морской транспорт;": "water",
            "вертолет": "helicopter",
        }
        self.lang = dict(ru="ru_RU", ua="ua_UA", )
        self.forma = "json"
        self.transfers = "false"

        self.__api_key = "you key"
        self._url = "https://api.rasp.yandex.net/v3.0/search?"
        self._data = {
            "from": "",
            "to": "",
            "lang": "",
            "date": " ",
            "transport_types": "",
            "transfers": "false",

        }

        self._date: int = 0

        logging.info("set")

        self.url = ""

    def bild_url(self):
        self.url = f"""{self._url}apikey={self.__api_key}&from={self._data['from']}&to={self._data['to']}&lang={
        self._data['lang']}&transfers={self.transfers}&transport={self._data["transport_types"]}"""
        log.warning(self.url)

    
    async def request(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                log.info(self.url)
                log.warning(response.status)
                log.info(response)

    def set_date(self, date: str):
        self._date = date

    def set_route(self, fm: str, to: str):
        self._data["from"] = fm
        self._data["to"] = to

    def close(self):
        del self._data["from"], \
            self._data["to"], \
            self.url

    def set_lang(self, lang: str):
        self._data["lang"] = self.lang[lang]

    def set_transport(self, transports: str):
        self._data["transport_types"] = self.transport[transports]

    async def get_code(self):
        url: str = f"https://api.rasp.yandex.net/v3.0/stations_list?apikey={self.__api_key}&format={self.forma}&lang=" \
            f"{self.lang['ru']}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                j = json.loads(str(await response.text()), encoding='UTF-8')
                json.dumps(j, indent=4, sort_keys=True)
                log.warning(j)
                with open("api.json", "w", encoding='UTF-8') as f:
                    f.write(str(j).replace("b","").replace("'"),"\n")_date: int = 0


        logging.info("set")

        self.url = ""

    def bild_url(self):
        self.url = f"""{self._url}apikey={self.__api_key}&from={self._data['from']}&to={self._data['to']}&lang={self._data['lang']}&transfers={self.transfers}"""
        print(self.url)

    def code(self):
        pass

    async def request(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                print(response.status)

    def set_date(self, date:str):
        self._date = date

    def set_route(self, fm:str, to:str):
        self._data["from"] = fm
        self._data["to"] = to

    def close(self):
        del self._data["from"], \
            self._data["to"], \
            self.url, \
