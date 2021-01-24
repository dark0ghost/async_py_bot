# This Python file uses the following encoding: utf-8
from pprint import pformat
from typing import Tuple, Dict, Union, Any
import os

import aiohttp
import ujson as json
from aiogram import Bot, types

# or config.json
with open("config.json", "r") as file:
    file_dict = json.loads(file.read())

token: str = os.environ.get("TOKEN")

PAYMENTS_PROVIDER_TOKEN: str = os.environ.get("PAYMENTS_PROVIDER_TOKEN")

TOKEN_QIWI: str = os.environ.get("TOKEN_QIWI")

POSTGRES: str = os.environ.get("POSTGRES")

lang: Tuple[str, str, str] = tuple(file_dict['lang'])

mes: Dict[str, str] = file_dict["mes"]

smtp_login: str = file_dict["smtp"]["login"]
smtp_password: str = file_dict["smtp"]["password"]
smtp_host: str = file_dict["smtp"]["host"]
smtp_port: int = int(file_dict["smtp"]["port"])

key: str = file_dict["key_accept"]

google_token: str = file_dict["google"]["key"]
domain = file_dict["web"]["domain"]

cat_api = os.environ.get("cat_api")

pastebian = os.environ.get("pastebin")


virustotal = os.environ.get("virustotal")

#master = file_dict["master"]
ether_api: Union[str, slice] = os.environ.get("etcherscan")


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
