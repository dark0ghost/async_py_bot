from asyncio.events import AbstractEventLoop
import asyncproxy
import asyncio
import orm_async_sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import help
import aiohttp
import logging
from aiosocksy.connector import ProxyConnector, ProxyClientRequest

proxy_list = []
logging.basicConfig(filename="log_base.log")


async def setproxy():
    connector = ProxyConnector()
    li = await asyncproxy.main()
    for proxy in li:
        try:
           async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session:
               async with session.get("https://google.com", proxy=proxy ) as response:
                    proxy_list.append(proxy)
                    print(2)
        except Exception as e:
            logging.exception(e)
            logging.info(f"warning {proxy} not valid")
            logging.debug(f"{proxy} valid")
            continue
    if len(proxy_list) <2:
        await setproxy()
        logging.info(f"log new rec")
        print(1)

loop: AbstractEventLoop = asyncio.get_event_loop()

db: orm_async_sqlite3 = orm_async_sqlite3.sqlite(connect="data3.db3")

state: orm_async_sqlite3 = orm_async_sqlite3.State(table="state", db=db)

asyncio.run(db.create_teblae())
asyncio.run(state.crt())
asyncio.run(setproxy())

print(proxy_list[0])
bot = Bot(token=help.token, loop=loop, proxy=proxy_list[1],)
dp = Dispatcher(bot)





@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, text=help.mes["start"],)




@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, text=help.mes["help"],)







if __name__ == '__main__':
    print("start")
    executor.start_polling(dp)


