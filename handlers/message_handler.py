# This Python file uses the following encoding: utf-8

import filter
import help
import price

from aiogram import types
from aiogram.types.message import ContentTypes
from model import async_proxy, E_mail
from typing import List
from aiogram.types import ContentType, User
from aiogram.dispatcher import FSMContext
from main import db, dp, bot, state, Button, keyboard,lazy_gettext, cb, session
from model.i18n import i18n


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    m = message.get_args()
    print(m)
    await  state.geo.set()
    await bot.send_message(message.chat.id, text=help.mes['start'], )


@dp.message_handler(commands=['language'])
async def cmd_language(message: types.Message, state: FSMContext):
    # track('command', message.from_user, command='language')
    await state.set_state('wait_language')
    await message.reply(
        lazy_gettext('Choose the language in which you are more comfortable to communicate'),
        reply_markup=keyboard.get_lang(lang)
    )


@dp.message_handler(state='wait_language')
async def wait_language(message: types.Message, state: FSMContext, user: User):
    # track('command', message.from_user, command='done_language')
    if message.text in lang:
        await user.set_language(message.text)
        lazy_gettext.ctx_locale.set(message.text)
        await message.reply(lazy_gettext('New language is: <b>English</b>'), reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.reply(lazy_gettext('Bad choice.'), reply_markup=keyboard.get_lang(lang))


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, text=help.mes["help"], )


@dp.message_handler(commands=['proxy'])
async def check_language(message: types.Message):
    proxy_list = await async_proxy.main(session)
    print(message.chat.id)
    await bot.send_message(message.chat.id, text=proxy_list[0],
                           reply_markup=Button.edit_proxy(proxy=proxy_list[0], text_button="not valid?",
                                                          callback="edit"))
    proxy_list.pop(0)


@dp.message_handler(commands=['proxy_all'])
async def check_language(message: types.Message):
    proxy_list: List[str] = await async_proxy.main(session=session)
    await bot.send_message(message.chat.id, text=lazy_gettext("text"),
                           reply_markup=Button.proxy(proxy_list))


@dp.message_handler(text=lazy_gettext(singular="курсы валют", enable_cache=False))
async def get_val(message: types.Message):
    date = await cb.Bild()
    await message.reply(text=lazy_gettext(singular="доступные валюты", enable_cache=False),
                        reply_markup=Button.buttons(Button, text=list(date.keys()), call_back=list(date.keys())))


@dp.message_handler(commands=["re"])
async def remove_board(message: types.Message):
    await bot.send_message(message.chat.id, text=lazy_gettext("del board"), reply_markup=keyboard.remove_kaeyboard())


@dp.message_handler(commands=["log"])
async def log(message: types.Message):
    if filter.is_master(message):
        await bot.send_document(message.chat.id, document=open("./log_base.log"))


# await bot.send_file("./log_base.log")


@dp.message_handler(state=state.mail)
async def get_mail(message: types.Message, state1: FSMContext):
    e: E_mail.e_mail = E_mail.e_mail(message.text)
    if e.is_e_mail():
        message.reply(lazy_gettext("good"))
        state1.finish()
        """
        todo: smtp requests

        """
    else:
        bot.send_message(message.chat.id, text=lazy_gettext("{message} bad mail").format(message=message.text))

    del e


@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    print("buy")
    await bot.send_invoice(message.chat.id, title='donate',
                           description='donate',
                           provider_token=help.PAYMENTS_PROVIDER_TOKEN,
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
async def got_payment(message: types.Message):
    await bot.send_message(message.chat.id, text=lazy_gettext(help.mes["buy"]),
                           parse_mode='Markdown')