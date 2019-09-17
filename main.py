# This Python file uses the following encoding: utf-8
from asyncio.events import AbstractEventLoop
from typing import List

from gino import Gino

import help
import aiohttp
import logging
import asyncio
import filter

from model import async_proxy, button, keyboard, i18n, cb_api, Crypto_Price, db_pg, CheckerEmail
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import Bot, Dispatcher, types
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from State import States

print("build")
# start set
postgres: Gino = db_pg.db_pg

checker_mail: CheckerEmail.CheckerEmail = CheckerEmail.CheckerEmail(hostname_mail=help.smtp_host,
                                                                    port=help.smtp_port, password=help.smtp_password,
                                                                    login=help.smtp_login)

checker_mail.change_len_code(new_len_code=5)

session: aiohttp.ClientSession = aiohttp.ClientSession()

crypto_price: Crypto_Price.CryptoPrice = Crypto_Price.CryptoPrice(session)

debug = True

cb = cb_api.CenterBankApi(session)

logging.basicConfig(filename="log_base.log", level=logging.INFO)

log = logging.getLogger("bot")

State = States()

Button = button.Button()

keyboard = keyboard.keyboard

proxy_list: List[str] = []

posts_cb = CallbackData('post', 'id', 'action')

Button.posts_cb = posts_cb

Base_filter: filter.Base_bot_filter = filter.Base_bot_filter()

lazy_get_text = i18n.lazy_gettext

lang: List[str] = []

"""if debug:
    storage = MemoryStorage()
else:
    storage = RedisStorage2()
"""
storage = MemoryStorage()


# start def

async def setproxy(session: aiohttp.ClientSession) -> List[str]:
    proxy_list = []
    connector = ProxyConnector()
    li = await async_proxy.main(session)
    for proxy in li:
        try:
            async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session:
                async with session.get("https://www.telegram.org", proxy=proxy) as response:
                    log.debug(f"{proxy} valid")
                    proxy_list.append(proxy)
                    help.good_proxy.append(proxy)

        except Exception as e:
            logging.exception(e)
            log.info(f"warning {proxy} not valid")

    if len(proxy_list) < 2:
        log.info(f"log new rec")
        await setproxy()


async def task():
    await postgres.set_bind(help.POSTGRES)
    await postgres.gino.create_all()

    global lang

    # lang = await


# end def

"""
fix :
RuntimeError: There is no current event loop in thread 'MainThread'.
"""
loop: AbstractEventLoop = asyncio.get_event_loop()

bot = Bot(token=help.token, loop=loop,
          parse_mode=types.ParseMode.MARKDOWN,
          proxy=help.good_proxy_link, proxy_auth=help.login)

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(i18n.i18n)


# asyncio.run(task())


# end set


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await session.close()
