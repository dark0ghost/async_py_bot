# This Python file uses the following encoding: utf-8
from typing import List

import help
import aiohttp
import logging
import asyncio


from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from model import async_proxy, orm_async_sqlite3,E_mail,button as b,keyboard
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, md, types
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

print("bild")
# startset
logging.basicConfig(filename="log_base.log", level=logging.DEBUG)
log = logging.getLogger("bot")
state = help.state()
button = b.button
keyboard = keyboard


# set proxy
async def setproxy():
    global proxy_list
    proxy_list = []
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

    if len(proxy_list) < 5:
        log.info(f"log new rec")
        await setproxy()


async def get_list_proxy():
    global list_proxy_inline
    list_proxy_inline = await async_proxy.main()
    print(list_proxy_inline)
    await asyncio.sleep(60)


"""
fix :

RuntimeError: There is no current event loop in thread 'MainThread'.

"""
loop = asyncio.get_event_loop()

db = orm_async_sqlite3.sqlite("data3.db3")

asyncio.run(db.create_teblae())

"""
  todo: db.create_contact
"""

# asyncio.run(setproxy())
bot = Bot(token=help.token, loop=loop, proxy=help.good_proxy_link, proxy_auth=help.login,
          parse_mode=types.ParseMode.MARKDOWN)

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


# endset

# message_handler
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    m = message.get_args()
    # await  state.conact.set()
    await bot.send_message(message.chat.id, text=help.mes['start'])


@dp.message_handler(state=state.start)
async def f(message: types.Message, state1: FSMContext):
    print(1)
    await state1.finish()
    await  bot.send_message(message.chat.id, text="state")


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, text=help.mes["help"], )


@dp.message_handler(commands=['proxy'])
async def check_language(message: types.Message):
    proxy: List[str] = await async_proxy.main()
    await bot.send_message(message.chat.id, text=help.mes["proxy"], reply_markup=button.proxy(proxy))


@dp.message_handler(content_types=ContentType.CONTACT)
async def getcontact(message: types.Message):
    """"
   todo: make db content
   """


@dp.message_handler(state=state.geo)
async def getgeo(message: types.Message, state1: FSMContext):
    state1.finish()
    pass


@dp.message_handler(commands=["re"])
async def remove_board(message: types.Message):
    await bot.send_message(message.chat.id, text="del board ", reply_markup=keyboard.remove_kaeyboard)


@dp.message_handler(state=state.mail)
async def get_mail(message: types.Message, state1: FSMContext):
    e: E_mail.e_mail = E_mail.e_mail(message.text)
    if e.is_e_mail():
        message.reply("готово")
        state1.finish()
        """
        todo: доделать записись в бд
        
        """
    else:
        bot.send_message(message.chat.id, text=f"{message.text} не является потчтой")

    del e


# end message_handler


# inline_handler

@dp.inline_handler()
async def inline_echo(inline_query: types.InlineQuery):
    input_content = types.InputTextMessageContent("{await async_proxy.main()} ")
    item = types.InlineQueryResultArticle(id='1', title=f'bot {inline_query.query}',
                                          input_message_content=input_content)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


# end inline_handler

# callback_query_handler

@dp.callback_query_handler()
async def back(message: types.Message):
    """
    todo
    :param message:
    :return:
    """


# end  callback_query_handler

if __name__ == '__main__':
    print("start")
    executor.start_polling(dp, on_shutdown=shutdown, loop=loop)
