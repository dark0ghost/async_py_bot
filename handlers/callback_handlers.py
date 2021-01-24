# This Python file uses the following encoding: utf-8

from aiogram import types

import helps
from core import posts_cb, dp, pastebin, io_json_box, postgres
from modules.db_pg import PastebinTable


@dp.callback_query_handler(posts_cb.filter(action=["pastebin"]))
async def pastebin_(query: types.CallbackQuery) -> None:
    paste = await PastebinTable.select("paste").where(PastebinTable.chat_id == query.message.chat.id).gino.scalar()
    h = pastebin.generate_data(paste=paste)
    link = await pastebin.send_paste(data=h)
    await query.message.edit_text(text=link)
    await paste.delete()


@dp.callback_query_handler(posts_cb.filter(action=["jsonbox"]))
async def json_box(query: types.CallbackQuery):
    await postgres.connect(helps.POSTGRES)
    text = await PastebinTable.select("paste").where(PastebinTable.chat_id == query.message.chat.id).gino.scalar()
    print(text)
    await query.message.edit_text(await io_json_box.create_box(
        text=text))
    await text.delete()
