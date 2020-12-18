# This Python file uses the following encoding: utf-8
import logging
import os
from typing import List

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from aiograph import Telegraph
from aiosocksy.connector import ProxyConnector, ProxyClientRequest

import filter
import helps
from modules import async_proxy, button, keyboard, i18n, ab_api, crypto_price, checker_email, cat_api, io_json_box, \
    db_pg, etherscan
from modules.com.pastebin import pastebin
from modules.com.virustotal.virustotal import Virustotal
from modules.org.ton.ton import TON
from modules.qrtag import QrTag
from set_loop import loop
from state import States

print("build")
# start set
postgres = db_pg.Postgres()

BASE_DIR: str = (os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/bot"

checker_mail: checker_email.CheckerEmail = checker_email.CheckerEmail(hostname_mail=helps.smtp_host,
                                                                      port=helps.smtp_port, password=helps.smtp_password,
                                                                      login=helps.smtp_login)
checker_mail.change_len_code(new_len_code=5)

telegraph = Telegraph()

session: aiohttp.ClientSession = aiohttp.ClientSession()

io_json_box: io_json_box = io_json_box.IOJsonBox(session)

crypto_price = crypto_price.CryptoPrice(session)

catApi = cat_api.CatApi(session=session)

ether_api: etherscan.EtherScan = etherscan.EtherScan(api_key=helps.ether_api, session=session)


debug = True

proxy_use: str = helps.proxy_use

pastebin: pastebin = pastebin.Pastebin(token=helps.pastebian, session=session)

ton = TON(session=session)

cb = ab_api.CenterBankApi(session)

logging.basicConfig(filename="log_base.log", level=logging.INFO)

log = logging.getLogger("bot")

State = States()

Button: button.Button = button.Button()

keyboard = keyboard.Keyboard

qr: QrTag = QrTag(session)

virustotal: Virustotal = Virustotal(session=session, api_key=helps.virustotal)

proxy_list: List[str] = []

posts_cb: CallbackData = CallbackData('post', 'id', 'action')

Button.posts_cb= posts_cb

Base_filter: filter.Base_bot_filter = filter.Base_bot_filter()
Master_filter: filter.MasterFilter = filter.MasterFilter()

lazy_get_text: i18n.lazy_gettext = i18n.lazy_gettext

lang: List[str] = []

proxy_class = async_proxy.Proxy(session=session)

"""
check debug on debug mode
"""
if debug:
    storage = MemoryStorage()
else:
    storage = RedisStorage2()


# start def
async def setproxy() -> None:
    """
    check  proxy and add to list
    @return:
    """
    proxy_box = []
    connector = ProxyConnector()
    li = await proxy_class.main()
    for proxy in li:
        try:
            async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session:
                async with session.get("https://www.telegram.org", proxy=proxy) as response:
                    log.debug(f"{proxy} valid")
                    proxy_box.append(proxy)

        except Exception as e:
            logging.exception(e)
            log.info(f"warning {proxy} not valid")

    if len(proxy_box) < 2:
        log.info(f"log new rec")
        await setproxy()


async def task():
    """
    connect to postgresql
    and telegraph
    @return:
    """
    bind = await postgres.connect(url=helps.POSTGRES)
    await telegraph.create_account((await bot.get_me())["first_name"])


# end def
if proxy_use:
    bot = Bot(token=helps.token, loop=loop,
              parse_mode=types.ParseMode.HTML,
              proxy=helps.good_proxy_link, proxy_auth=helps.login)
else:
    bot = Bot(token=helps.token, loop=loop,
              parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(i18n.i18n)

loop.run_until_complete(task())


# end set
async def shutdown(dispatcher: Dispatcher):
    """
    :param dispatcher:
    :return:
    """
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await session.close()
