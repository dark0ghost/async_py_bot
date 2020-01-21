# This Python file uses the following encoding: utf-8
from pprint import pformat

import aiohttp
import ujson as json

from aiogram import Bot, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from typing import Tuple, Dict, Union, Any

# or config.json
with open("config_pro.json", "r") as file:
    file_dict: Dict[str, str] = json.loads(file.read())

token: str = file_dict["token"]

PAYMENTS_PROVIDER_TOKEN: str = file_dict["PAYMENTS_PROVIDER_TOKEN"]

TOKEN_QIWI: str = file_dict["TOKEN_QIWI"]

POSTGRES: str = file_dict["POSTGRES"]

lang: Tuple[str, str, str] = tuple(file_dict['lang'])

mes: Dict[str, str] = file_dict["mes"]

good_proxy_link: str = file_dict["good_proxy_link"]
login: aiohttp.BasicAuth = aiohttp.BasicAuth(login=file_dict["login"]["login"], password=file_dict["login"]["password"])

smtp_login: str = file_dict["smtp"]["login"]
smtp_password: str = file_dict["smtp"]["password"]
smtp_host: str = file_dict["smtp"]["host"]
smtp_port: int = int(file_dict["smtp"]["port"])

key: str = file_dict["key_accept"]

google_token: str = file_dict["google"]["key"]
domain = file_dict["web"]["domain"]

cat_api = file_dict["cat_api"]["token"]

pastebian = file_dict["pastebin"]

proxy_use = file_dict["proxy_use"]

virustotal = file_dict["virustotal"]

master = file_dict["master"]
ether_api: Union[str, slice] = file_dict["etcherscan"]["token"]


async def get_link(bot: Bot, message: types.Message) -> str:
    """
     return ref link
    :param bot:
    :param message:
    :return:
    """
    link_bot = (await bot.get_me()).username

    link: str = f"t.me/{link_bot}/?ref={message.chat.id}"
    return link


def format_dict(object: Dict[Any, Any]):
    """
    format json for more reding
    @param object:
    @return:
    """
    return pformat(
        object
    ) \
        .replace(",", ",\n") \
        .replace("'", "") \
        .replace(
        "{",
        "{\n") \
        .replace(
        "}", "\n}") \
        .replace("[\n", "") \
        .replace("]", "\n]")
