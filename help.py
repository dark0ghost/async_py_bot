# This Python file uses the following encoding: utf-8
import aiohttp

from aiogram import Bot
from aiogram.dispatcher.filters.state import State, StatesGroup

from typing import Tuple

package: list = ["aiodns", "aiohttp", "async-timeout", "beautifulsoup4", "aiogram", "aiosqlite", "aiosocks",
                 "aiosocksy",
                 "aiohttp_socks"]

token: str = "545171444:AAHg8QcGzRxeW2TobW1oxV8lt_d2dKu-plA"

PAYMENTS_PROVIDER_TOKEN:str = "632593626:TEST:i56982357197"

lang: Tuple[str] = ("ru", "en", "ua")

mes: dict = {
    "start": "message start",
    "help": "message help",
    "proxy": "public proxy for you",
    "new_proxy":"new proxy",
    "buy":"покупка произведена успешно",
    "error_pay":"окупка не произошла",
}

good_proxy_link: str = "socks5://exp1.s5overss.mtpro.xyz:39610"
login = aiohttp.BasicAuth(login='mtpro_xyz', password='mtpro_xyz_bot')


async def get_link(bot: Bot):
    link_bot = (await bot.get_me()).username

    link: str = f"t.me/{link_bot}/?ref="
    return link

class state(StatesGroup):
    start: State = State()
    end: State = State()
    conact: State = State()
    geo: State = State()
    mail: State = State()
    pass



