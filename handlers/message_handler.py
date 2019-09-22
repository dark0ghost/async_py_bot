# This Python file uses the following encoding: utf-8

import filter
import help
import price
import faces as faceapp

from aiogram import types
from aiogram.types.message import ContentTypes
from model import async_proxy
from typing import List
from aiogram.types import ContentType, User
from aiogram.dispatcher import FSMContext
from main import dp, bot, State, Button, keyboard, lazy_get_text, cb, session, lang, checker_mail, BASE_DIR
from model.i18n import i18n


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    m = message.get_args()
    await State.get_mail.set()
    await bot.send_message(message.chat.id, text=help.mes['start'], )


@dp.message_handler(commands=['language'])
async def cmd_language(message: types.Message, state: FSMContext):
    # track('command', message.from_user, command='language')
    await state.set_state('wait_language')
    await message.reply(
        lazy_get_text('Choose the language in which you are more comfortable to communicate'),
        reply_markup=keyboard.get_lang(lang)
    )


@dp.message_handler(state='wait_language')
async def wait_language(message: types.Message, state: FSMContext, user: User):
    # track('command', message.from_user, command='done_language')
    if message.text in lang:
        await user.set_language(message.text)
        lazy_get_text.ctx_locale.set(message.text)
        await message.reply(lazy_get_text('New language is: <b>English</b>'), reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.reply(lazy_get_text('Bad choice.'), reply_markup=keyboard.get_lang(lang))


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
    await bot.send_message(message.chat.id, text=lazy_get_text("text"),
                           reply_markup=Button.proxy(proxy_list))


@dp.message_handler(text=lazy_get_text(singular="курсы валют", enable_cache=False))
async def get_val(message: types.Message):
    date = await cb.build_list_coin()
    await message.reply(text=lazy_get_text(singular="доступные валюты", enable_cache=False),
                        reply_markup=Button.buttons(Button, text=list(date.keys()), call_back=list(date.keys())))


@dp.message_handler(commands=["re"])
async def remove_board(message: types.Message):
    await bot.send_message(message.chat.id, text=lazy_get_text("del board"), reply_markup=keyboard.remove_kaeyboard())


@dp.message_handler(commands=["log"])
async def log(message: types.Message):
    if filter.is_master(message):
        await bot.send_document(message.chat.id, document=open("./log_base.log"))


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
    await bot.send_message(message.chat.id, text=lazy_get_text(help.mes["buy"]),
                           parse_mode='Markdown')


@dp.message_handler(state=State.get_mail)
async def get_mail(message: types.Message, state: FSMContext):
    await message.reply("send code")
    print(1)
    mail = message.text
    async with state.proxy() as data:
        data["passcode"] = checker_mail.get_random_code()
        checker_mail.build_message(text=data["passcode"], from_mail=help.smtp_login, to=mail, subject="test")

    await checker_mail.async_send_message(start_tls=1)
    await State.mail_ver.set()


@dp.message_handler(state=State.mail_ver)
async def V_mail(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == data["passcode"]:
            await message.reply("good")


        else:
            await message.reply("warning")


@dp.message_handler(commands="make")
async def facep(message: types.Message):
    file = open(BASE_DIR + "/staticfile/1.jpg", "rb")
    image = faceapp.FaceAppImage(file=file)
    happy = image.apply_filter('old', cropped=True)
    await message.reply(happy)
