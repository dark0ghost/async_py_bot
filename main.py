# This Python file uses the following encoding: utf-8
from asyncio.events import AbstractEventLoop
from typing import List

import help
import aiohttp
import logging
import asyncio
import filter

from model import async_proxy, orm_async_sqlite3, button, keyboard, i18n, cb_api, Crypto_Price
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram import Bot, Dispatcher, types
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData

print("bild")
# startset

session: aiohttp.ClientSession = aiohttp.ClientSession()

crypto_price = Crypto_Price.CryptoPrice(session)

debug = True

cb = cb_api.CenterBankApi(session)

logging.basicConfig(filename="log_base.log", level=logging.INFO)

log = logging.getLogger("bot")

state = help.state()

Button = button.Button()

keyboard = keyboard.keyboard

proxy_list: List[str] = []

posts_cb = CallbackData('post', 'id', 'action')

Button.posts_cb = posts_cb

Basefilter: filter.Base_bot_filter = filter.Base_bot_filter()

db: orm_async_sqlite3.sqlite = orm_async_sqlite3.sqlite("data_sqlite.db3")

lazy_gettext = i18n.lazy_gettext

lang: List[str] = []

if (debug):
    storage = MemoryStorage()
else:
    storage = RedisStorage2()


# start def
# set proxy
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


# asyncio.run(setproxy(session))

async def task():
    await db.create_teble()
    await db.create_teble_lang()
    # await db.insert_lang(lang='ru')
    # await db.insert_lang(lang='en')
    global lang
    lang = await db.get_lang()


# end def


"""
fix :
RuntimeError: There is no current event loop in thread 'MainThread'.
"""
loop: AbstractEventLoop = asyncio.get_event_loop()

"""
  todo: db.create_contact
"""

bot = Bot(token=help.token, loop=loop,
          parse_mode=types.ParseMode.MARKDOWN,
          proxy=help.good_proxy_link, proxy_auth=help.login, )

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# dp.filters_factory.bind(basefilter)
dp.middleware.setup(i18n.i18n)

asyncio.run(task())


# endset


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await session.close()
