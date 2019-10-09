# This Python file uses the following encoding: utf-8
import os
from asyncio.events import AbstractEventLoop
from typing import List

import helps
import aiohttp
import logging
import asyncio
import filter
import uvloop

from modules.com.pastebin import Pastebin
from modules import async_proxy, button, keyboard, i18n, cb_api, Crypto_Price, CheckerEmail, CatApi, IoJsonBox, db_pg
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import Bot, Dispatcher, types
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData


from State import States
from modules.org.ton.Ton import TON
from modules.qrtag import QrTag


print("build")
# start set
postgres = db_pg.Postgres()

BASE_DIR: str = (os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/bot"

checker_mail: CheckerEmail.CheckerEmail = CheckerEmail.CheckerEmail(hostname_mail=helps.smtp_host,
                                                                    port=helps.smtp_port, password=helps.smtp_password,
                                                                    login=helps.smtp_login)

checker_mail.change_len_code(new_len_code=5)

session: aiohttp.ClientSession = aiohttp.ClientSession()

io_json_box: IoJsonBox = IoJsonBox.IOJsonBox(session)

crypto_price: Crypto_Price.CryptoPrice = Crypto_Price.CryptoPrice(session)

catApi = CatApi.CatApi(session=session)

debug = True

proxy_use: str = helps.proxy_use

pastebin: Pastebin = Pastebin.Pastebin(token=helps.pastebian, session=session)

ton = TON(session=session)

cb = cb_api.CenterBankApi(session)

logging.basicConfig(filename="log_base.log", level=logging.INFO)

log = logging.getLogger("bot")

State = States()

Button: button.Button = button.Button()

keyboard = keyboard.Keyboard

qr = QrTag(session)

proxy_list: List[str] = []

posts_cb: CallbackData = CallbackData('post', 'id', 'action')

Button.posts_cb = posts_cb

Base_filter: filter.Base_bot_filter = filter.Base_bot_filter()

lazy_get_text: i18n.lazy_gettext = i18n.lazy_gettext

lang: List[str] = []

if debug:
    storage = MemoryStorage()
else:
    storage = RedisStorage2()


# start def

async def setproxy(session: aiohttp.ClientSession) -> None:
    proxy_list = []
    connector = ProxyConnector()
    li = await async_proxy.main(session)
    for proxy in li:
        try:
            async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session:
                async with session.get("https://www.telegram.org", proxy=proxy) as response:
                    log.debug(f"{proxy} valid")
                    proxy_list.append(proxy)


        except Exception as e:
            logging.exception(e)
            log.info(f"warning {proxy} not valid")

    if len(proxy_list) < 2:
        log.info(f"log new rec")
        await setproxy()


async def task():
    bind = await postgres.connect(url=helps.POSTGRES)

    global lang

    # lang = await


# end def

"""
fix :
RuntimeError: There is no current event loop in thread 'MainThread'.
"""
loop: AbstractEventLoop = asyncio.get_event_loop()

if proxy_use == "True":
    bot = Bot(token=helps.token, loop=loop,
              parse_mode=types.ParseMode.MARKDOWN,
              proxy=helps.good_proxy_link, proxy_auth=helps.login)
else:
    bot = Bot(token=helps.token, loop=loop,
              parse_mode=types.ParseMode.MARKDOWN, proxy="socks5://207.180.238.12:1080")

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(i18n.i18n)

asyncio.run(task())


# end set


async def shutdown(dispatcher: Dispatcher):
    """

    :param dispatcher:
    :return:
    """
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await session.close()
