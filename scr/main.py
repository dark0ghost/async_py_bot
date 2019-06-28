# This Python file uses the following encoding: utf-8


from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

import help
import aiohttp
import logging
import asyncio
import button as b

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from model import async_proxy, orm_async_sqlite3
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
keyboard = b.keyboard


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


"""
fix :

RuntimeError: There is no current event loop in thread 'MainThread'.

"""
loop = asyncio.get_event_loop()

db = orm_async_sqlite3.sqlite("data3.db3")

asyncio.run(db.create_teblae())
# asyncio.run(setproxy())
bot = Bot(token=help.token, loop=loop, proxy=help.good_proxy_link, proxy_auth=help.login,
          parse_mode=types.ParseMode.MARKDOWN)

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


# endset

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    m = message.get_args()
    #await  state.conact.set()
    await bot.send_message(message.chat.id, text=help.mes['start'],reply_markup=keyboard.get_contact()) #reply_markup=button.start())


@dp.message_handler(state=state.start)
async def f(message: types.Message, state1: FSMContext):
    print(1)
    await state1.finish()
    await  bot.send_message(message.chat.id, text="state")


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, text=help.mes["help"], )


@dp.callback_query_handler()
async def back(message: types.Message):
    pass


@dp.message_handler(commands=['h'])
async def check_language(message: types.Message):
    locale = message.from_user.locale
    print(1)
    await message.reply(md.text(
        md.bold('Info about your language:'),
        md.text(' d', md.bold('Code:'), md.italic(locale.locale)),
        md.text(' q', md.bold('Territory:'), md.italic(locale.territory or 'Unknown')),
        md.text(' p', md.bold('Language name:'), md.italic(locale.language_name)),
        md.text(' t', md.bold('English language name:'), md.italic(locale.english_name)),
        sep='\n'))
    print(2)


@dp.inline_handler()
async def inline_echo(inline_query: types.InlineQuery):
    print(1)
    input_content = types.InputTextMessageContent("{await async_proxy.main()} ")
    item = types.InlineQueryResultArticle(id='1', title=f'bot {inline_query.query}',
                                          input_message_content=input_content)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

@dp.message_handler(content_types=ContentType.CONTACT)
async def getcontact(message: types.Message):

     print(message.contact)

@dp.message_handler(state=state.geo)
async def getgeo(message: types.Message,state1: FSMContext):
     state1.finish()

     print(message.text)

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    print("start")
    executor.start_polling(dp, on_shutdown=shutdown, loop=loop, )
