# This Python file uses the following encoding: utf-8
import aiohttp

from aiogram import Bot, types
from aiogram.dispatcher.filters.state import State, StatesGroup

from typing import Tuple

token: str = "545171444:AAHSsUCR8Z1rgC9qb_sUzWdGo6nOvH5Msoo"

PAYMENTS_PROVIDER_TOKEN: str = "632593626:TEST:i56982357197"

QIWI_TOKEN: str = ""

POSTGRES: str = "postgresql://postgres:A3dSA24Dctf2v4HE@eventstracker:5432/postgres"
lang: Tuple[str] = ("ru", "en", "ua")

mes: dict = {
    "start": "message start",
    "help": "message help",
    "proxy": "public proxy for you",
    "new_proxy": "new proxy",
    "buy": "покупка произведена успешно",
    "error_pay": "покупка не произошла",
}

good_proxy_link: str = "socks5://orbtl.s5.opennetwork.cc:999"
login = aiohttp.BasicAuth(login='387544140', password='w61D1u5v')


async def get_link(bot: Bot, message: types.Message):
    link_bot = (await bot.get_me()).username

    link: str = f"t.me/{link_bot}/?ref={message.chat.id}"
    return link


class state(StatesGroup):
    start: State = State()
    end: State = State()
    contact: State = State()
    geo: State = State()
    mail: State = State()
