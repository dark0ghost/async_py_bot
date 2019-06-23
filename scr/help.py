package: list = ["aiodns", "aiohttp", "async-timeout", "beautifulsoup4", "aiogram", "aiosqlite", "aiosocks",
                 "aiosocksy",
                 "aiohttp_socks"]

token: str = ""

mes: dict = {
    "start": "message start",
    "help": "message help",

}
import aiohttp
good_proxy_link: str = "socks5://exp1.s5overss.mtpro.xyz:39610"
login = aiohttp.BasicAuth(login='mtpro_xyz', password='mtpro_xyz_bot')

from aiogram.utils.helper import Helper, HelperMode, ListItem


class state(Helper):
    mode = HelperMode.snake_case
    END = ListItem()
    START = ListItem()
    pass

