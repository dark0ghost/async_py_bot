# This Python file uses the following encoding: utf-8
import asyncio
import aiohttp
import logging

logging.basicConfig(filename="yandex_api.log")


class transport:
    transport = {
        "самолет": "plane",
        "поезд": "train",
        "электричка": "suburban",
        "автобус": "bus",
        "морской транспорт;": "water",
        "вертолет": "helicopter",
    }
    lang = dict(ru="ru_RU", ua="ua_UA", )

    def __init__(self, *args):
        self.forma = "json"
        self.transfers = "false"

        self.__api_key = " "
        self._url = "https://api.rasp.yandex.net/v3.0/search?"
        self._data = {
            "from": "",
            "to": "",
            "lang": "",
            "date": " ",
            "transport_types": "",
            "transfers":"false",



        }
        self._date: int = 0


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
