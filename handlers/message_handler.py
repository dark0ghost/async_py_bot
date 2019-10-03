# This Python file uses the following encoding: utf-8
import html
import os
from pprint import pformat
from typing import List, Any

import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import User
from aiogram.types.message import ContentTypes

import filter
import helps
import price

from core import dp, bot, State, Button, keyboard, lazy_get_text, cb, session, lang, checker_mail, catApi, io_json_box, \
    pastebin, postgres
from model import async_proxy
from model.db_pg import PastebinTable


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message) -> None:
    m = message.get_args()
    await State.get_mail.set()
    await bot.send_message(message.chat.id, text=helps.mes['start'],
                           reply_markup=keyboard.keyboard_all(lazy_get_text("отмена")))


@dp.message_handler(commands=['language'])
async def cmd_language(message: types.Message, state: FSMContext) -> None:
    # track('command', message.from_user, command='language')
    await state.set_state('wait_language')
    await message.reply(
        lazy_get_text('Choose the language in which you are more comfortable to communicate'),
        reply_markup=keyboard.get_lang(lang)
    )


@dp.message_handler(state='wait_language')
async def wait_language(message: types.Message, state: FSMContext, user: User) -> None:
    # track('command', message.from_user, command='done_language')
    if message.text in lang:
        await user.set_language(message.text)
        lazy_get_text.ctx_locale.set(message.text)
        await message.reply(lazy_get_text('New language is: <b>English</b>'), reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.reply(lazy_get_text('Bad choice.'), reply_markup=keyboard.get_lang(lang))


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message) -> None:
    await bot.send_message(message.chat.id, text=helps.mes["help"], )


@dp.message_handler(commands=['proxy'])
async def check_language(message: types.Message) -> None:
    proxy_list = await async_proxy.main(session)
    print(message.chat.id)
    await bot.send_message(message.chat.id, text=proxy_list[0],
                           reply_markup=Button.edit_proxy(proxy=proxy_list[0], text_button="not valid?",
                                                          callback="edit"))
    proxy_list.pop(0)


@dp.message_handler(commands=['proxy_all'])
async def check_language(message: types.Message) -> None:
    proxy_list: List[str] = await async_proxy.main(session=session)
    await bot.send_message(message.chat.id, text=lazy_get_text("text"),
                           reply_markup=Button.proxy(proxy_list))


@dp.message_handler(text=lazy_get_text(singular="курсы валют", enable_cache=False))
async def get_val(message: types.Message) -> None:
    date = await cb.build_list_coin()
    await message.reply(text=lazy_get_text(singular="доступные валюты", enable_cache=False),
                        reply_markup=Button.buttons(Button, text=list(date.keys()), call_back=list(date.keys())))


@dp.message_handler(commands=["re"])
async def remove_board(message: types.Message) -> None:
    await bot.send_message(message.chat.id, text=lazy_get_text("del board"), reply_markup=keyboard.remove_keyboard())


@dp.message_handler(commands=["log"])
async def log(message: types.Message) -> None:
    if filter.is_master(message):
        await bot.send_document(message.chat.id, document=open("./log_base.log"))


@dp.message_handler(commands=['buy'])
async def buy(message: types.Message) -> None:
    print("buy")
    await bot.send_invoice(message.chat.id, title='donate',
                           description='donate',
                           provider_token=helps.PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           photo_url='https://e3.edimdoma.ru/data/recipes/0006/0497/60497-ed4_wide.jpg?1468399744',
                           photo_height=512,  # !=0/None or picture won't be shown
                           photo_width=512,
                           photo_size=512,
                           # is_flexible=1,  # True If you need to set up Shipping Fee
                           prices=price.price,
                           start_parameter='time-machine-example',
                           payload='HAPPY FRIDAYS COUPON')


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message) -> None:
    await bot.send_message(message.chat.id, text=lazy_get_text(helps.mes["buy"]),
                           parse_mode='Markdown')


@dp.message_handler(state=State.get_mail)
async def get_mail(message: types.Message, state: FSMContext) -> None:
    if message.text != lazy_get_text("отмена"):
        await message.reply("send code")
        print(1)
        mail = message.text
        async with state.proxy() as data:
            data["passcode"] = checker_mail.get_random_code()
            checker_mail.build_message(text=data["pass_code"], from_mail=helps.smtp_login, to=mail, subject="test")

        await checker_mail.async_send_message(start_tls=True)
        await State.mail_ver.set()
    await message.reply(text=lazy_get_text("ok"), reply_markup=keyboard.remove_keyboard())
    await state.finish()


@dp.message_handler(state=State.mail_ver)
async def V_mail(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text == data["pass_code"]:
            await message.reply("good")
        else:
            await message.reply("warning")


@dp.message_handler(commands=["cat"])
async def cat(message: types.Message) -> None:
    print(os.path.abspath("staticfile/cat.jpg"))
    await catApi.get_photo()
    await bot.send_photo(chat_id=message.chat.id,
                         photo=open(os.path.abspath("staticfile/cat.jpg"), "rb"))


@dp.message_handler(commands=["json"])
async def save_json(message: types.Message) -> None:
    try:
        await message.reply(await io_json_box.create_box(text=message.reply_to_message.text))
        return
    except Exception as e:
        print(e)
        await State.save_json.set()
        await message.reply(lazy_get_text("send json"))


@dp.message_handler(state=State.save_json)
async def save_json(message: types.Message, state: FSMContext) -> None:
    await message.reply(await io_json_box.create_box(text=message.text))
    await state.finish()


@dp.message_handler(commands=["search_json"])
async def search_json(message: types.Message) -> None:
    try:
        await message.reply(
            (pformat(await io_json_box.get_data_link(url=message.reply_to_message.text))).replace(",", ",\n").replace(
                "'", "").replace(
                "{",
                "{\n").replace(
                "}", "\n}").replace("[\n", "").replace("]", "\n]"),
            parse_mode=types.ParseMode.MARKDOWN)

    except Exception:
        await State.search_json.set()
        await message.reply(lazy_get_text("send URL json"),
                            reply_markup=keyboard.keyboard_all(text=lazy_get_text("no search")))


@dp.message_handler(state=State.search_json)
async def save_json(message: types.Message, state: FSMContext) -> None:
    if message.text != "no search":
        await message.reply(
            (pformat(await io_json_box.get_data_link(url=message.text))).replace(",", ",\n").replace("'", "").replace(
                "{",
                "{\n").replace(
                "}", "\n}").replace("[\n", "").replace("]", "\n]"),
            parse_mode=types.ParseMode.MARKDOWN, reply_markup=keyboard.remove_keyboard())
    else:
        await message.reply(lazy_get_text("ok"), reply_markup=keyboard.remove_keyboard())
    await state.finish()


@dp.message_handler(commands=["paste"])
async def return_paste(message: types.Message) -> None:
    try:

        await message.reply(await pastebin.send_paste(data=pastebin.generate_data(paste=message.reply_to_message.text)))
    except Exception as e:
        await State.send_paste.set()
        await message.reply(lazy_get_text(f"send paste"))


@dp.message_handler(state=State.send_paste)
async def _paste(message: types.Message, state: FSMContext):
    h = pastebin.generate_data(paste=message.text)
    await message.reply(await pastebin.send_paste(data=h))
    return await state.finish()


@dp.message_handler(commands=["make_paste"])
async def make_paste(message: types.Message) -> Button.buttons:

    await postgres.connect(helps.POSTGRES)

    s = await PastebinTable.create(paste=message.reply_to_message.text, chat_id=message.chat.id)
    print(s)
    return await message.answer(text=lazy_get_text("какой формат?"),
                                reply_markup=Button.buttons(text=["pastebin", "jsonbox"],
                                                            call_back=["pastebin",
                                                                       "jsonbox"]))


"""except Exception as e:
        # await message.reply(text=lazy_get_text("no replay message"))
        await message.reply(e)
        return None"""
