
from aiogram import Bot
from aiogram.dispatcher.filters.state import State, StatesGroup

package: list = ["aiodns", "aiohttp", "async-timeout", "beautifulsoup4", "aiogram", "aiosqlite", "aiosocks",
                 "aiosocksy",
                 "aiohttp_socks"]

token: str = ""

mes: dict = {
    "start": "message start",
    "help": "message help",

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
    geo:State = State()
    pass
