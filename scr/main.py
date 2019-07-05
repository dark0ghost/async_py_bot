# This Python file uses the following encoding: utf-8
from asyncio.events import AbstractEventLoop
from typing import List

import help
import aiohttp
import logging
import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from model import async_proxy, orm_async_sqlite3, E_mail, button, keyboard
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, md, types
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified, Throttled
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

print("bild")
# startset
logging.basicConfig(filename="log_base.log", level=logging.INFO)
log = logging.getLogger("bot")
state = help.state()
Button = button.Button
keyboard = keyboard.keyboard
proxy_list: List[str] = []
posts_cb = CallbackData('post', 'id', 'action')
Button.posts_cb = posts_cb


# start def
# set proxy
async def setproxy() -> List[str]:
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


# end def


"""
fix :

RuntimeError: There is no current event loop in thread 'MainThread'.

"""
loop: AbstractEventLoop = asyncio.get_event_loop()

db: orm_async_sqlite3.sqlite = orm_async_sqlite3.sqlite("data3.db3")

asyncio.run(db.create_teblae())

"""
  todo: db.create_contact
"""

# asyncio.run(setproxy())
bot = Bot(token=help.token, loop=loop,
          parse_mode=types.ParseMode.MARKDOWN,) #proxy=help.good_proxy_link, proxy_auth=help.login,)

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
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
    await state1.finish()
    await bot.send_message(message.chat.id, text="state")


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, text=help.mes["help"], )


@dp.message_handler(commands=['proxy'])
async def check_language(message: types.Message):
    proxy_list = await async_proxy.main()
    await  bot.send_message(message.chat.id, text="text",
                            reply_markup=Button.edit_proxy(proxy=proxy_list[0], text_button="не работает?",
                                                           callback="edit"))
    proxy_list.pop(0)

@dp.message_handler(commands=['proxy_all'])
async def check_language(message: types.Message):
    proxy_list: List[str] = await async_proxy.main()
    await bot.send_message(message.chat.id, text="text",
                            reply_markup=Button.proxy(proxy_list))

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
    await bot.send_message(message.chat.id, text="del board ", reply_markup=keyboard.remove_kaeyboard())

@dp.message_handler(commands=["log"])
async def log(message: types.Message):
    with open("log_base.log","r") as f:
        message.reply(f.read())

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
    """if len(proxy_list) < 1:
        item = types.InlineQueryResultArticle(id='1', title='нет прокси',
                                              input_message_content=input_content)
        await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
        #[proxy_list.append(i) for i in await async_proxy.main()]
    else:
        item = types.InlineQueryResultArticle(id='1', title=f'bot {inline_query.query}',
                                              input_message_content=input_content,
                                              reply_markup=Button.edit_proxy(text_button="не работает?",
                                                                             proxy=proxy_list[0],
                                                                             callback="edit"))
        await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
    """

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


# end inline_handler

# callback_query_handler

@dp.callback_query_handler(posts_cb.filter(action=['edit']))
async def back(query: types.CallbackQuery, callback_data: dict):
    """
    todo
    :param message:
    :return:
    """
    print("starts")

    if len(proxy_list) < 1:
        [proxy_list.append(i) for i in await async_proxy.main()]
    else:
        await query.message.edit_text(text=help.mes["new_proxy"],
                                      reply_markup=Button.edit_proxy(text_button="не работает?", proxy=proxy_list[0],
                                                                     callback="edit"))
        proxy_list.pop(0)
    print("end")

    # end  callback_query_handler


if __name__ == '__main__':
    print("start")
    executor.start_polling(dp, on_shutdown=shutdown, loop=loop)
