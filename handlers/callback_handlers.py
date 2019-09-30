# This Python file uses the following encoding: utf-8
from typing import Dict

import help

from main import posts_cb, proxy_list, Button, dp, session, pastebin, io_json_box,pastebin_table
from model import async_proxy
from aiogram import types


@dp.callback_query_handler(posts_cb.filter(action=['edit']))
async def back(query: types.CallbackQuery):
    """
    :param query:
    :return:
    """
    if len(proxy_list) < 1:
        [proxy_list.append(i) for i in await async_proxy.main(session=session)]
    else:
        await query.message.edit_text(text=help.mes["new_proxy"],
                                      reply_markup=Button.edit_proxy(text_button="не работает?", proxy=proxy_list[0],
                                                                     callback="edit"))
        proxy_list.pop(0)


@dp.callback_query_handler(posts_cb.filter(action=["pastebin"]))
async def pastebin_(query: types.CallbackQuery) -> None:
    print(await pastebin_table.query.where(pastebin_table.chat_id.contains(query.message.chat.id)).gino.all())
    h = pastebin.generate_data(paste=query.message.text)
    link = await pastebin.send_paste(data=h)
    await query.message.edit_text(text=link)


@dp.callback_query_handler(posts_cb.filter(action=["jsonbox"]))
async def json_box(query: types.CallbackQuery):
    print(await pastebin_table.query.where(pastebin_table.chat_id.contains(query.message.chat.id)).gino.all())
