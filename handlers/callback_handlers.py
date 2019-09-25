# This Python file uses the following encoding: utf-8
import help

from main import posts_cb, proxy_list, Button, dp, session
from model import async_proxy
from aiogram import types



@dp.callback_query_handler(posts_cb.filter(action=['edit']))
async def back(query: types.CallbackQuery, callback_data: dict):
    """
    :param callback_data:
    :param message:
    :return:
    """
    if len(proxy_list) < 1:
        [proxy_list.append(i) for i in await async_proxy.main(session=session)]
    else:
        await query.message.edit_text(text=help.mes["new_proxy"],
                                      reply_markup=Button.edit_proxy(text_button="не работает?", proxy=proxy_list[0],
                                                                     callback="edit"))
        proxy_list.pop(0)
