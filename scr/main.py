# This Python file uses the following encoding: utf-8

import help
import aiohttp
import logging
import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from model import async_proxy
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
from model import orm_async_sqlite3

print("bild")

logging.basicConfig(filename="log_base.log",level=logging.DEBUG)
log = logging.getLogger("bot")


async def setproxy():
    global proxy_list
    proxy_list= []
    connector = ProxyConnector()
    li = await async_proxy.main()
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
            print(f"warning {proxy} not valid")

    if len(proxy_list) < 5:
        log.info(f"log new rec")
        await setproxy()


loop = asyncio.get_event_loop()

db = orm_async_sqlite3.sqlite("data3.db3")


asyncio.run(db.create_teblae())
#asyncio.run(setproxy())

bot = Bot(token=help.token, loop=loop,proxy=help.good_proxy_link,proxy_auth=help.login)

dp = Dispatcher(bot,storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, text=help.mes["start"], )


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, text=help.mes["help"], )

@dp.callback_query_handler()
async def back(message: types.Message):
    pass


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


@dp.message_handler( commands=['setstate'])
async def process_setstate_command(message: types.Message):
   
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(message['state_reset'])

    if (not argument.isdigit()) or (not int(argument) < len(help.state.all())):
        return await message.reply(message['invalid_key'].format(key=argument))
    print(state)
    await state.set_state(help.state.all()[int(argument)])
    await message.reply(message['state_change'], reply=False)



if __name__ == '__main__':
    print("start")
    executor.start_polling(dp,on_shutdown=shutdown)
