# This Python file uses the following encoding: utf-8
import aiohttp

from aiogram import Bot, types
from aiogram.dispatcher.filters.state import State, StatesGroup

from typing import Tuple

token: str = ""

PAYMENTS_PROVIDER_TOKEN: str = ""

TOKEN_QIWI: str = ""

POSTGRES: str = ""
lang: Tuple[str, str, str] = ("ru", "en", "ua")

mes: dict = {
    "start": "message start",
    "help": "message help",
    "proxy": "public proxy for you",
    "new_proxy": "new proxy",
    "buy": "покупка произведена успешно",
    "error_pay": "покупка не произошла",
}

good_proxy_link: str = "socks5://orbtl.s5.opennetwork.cc:999"
login: aiohttp.BasicAuth = aiohttp.BasicAuth(login='387544140', password='w61D1u5v')


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


