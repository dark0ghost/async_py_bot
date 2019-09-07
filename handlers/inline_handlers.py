# This Python file uses the following encoding: utf-8
import hashlib

from aiogram import types
from main import dp, bot, lazy_gettext, cb as bankapi, crypto_price
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery) -> InlineQueryResultArticle:
    # id affects both preview and content,
    # so it has to be unique for each result
    # (Unique identifier for this result, 1-64 Bytes)
    # you can set your unique id's
    # but for example i'll generate it based on text because I know, that
    # only text will be passed in this example
    text = inline_query.query
    res = await  bankapi.Bild()
    crypto = await crypto_price.coin_list()
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    if text in res.keys():
        input_content = InputTextMessageContent(lazy_gettext("""название {name}\n`стоимость 1 {name} - {valvue}₽`\n__дата {date}\n по данным центробанка (https://www.cbr.ru)__
        """).format(name=text, valvue=res[text]["valvue"], date=bankapi.date))

        item = InlineQueryResultArticle(
            id=result_id,
            title=lazy_gettext('{name} - {valvue}').format(name=text, valvue=res[text]["valvue"]),
            input_message_content=input_content
        )
    elif text in crypto:
        id_coin = crypto[text]["id"]
        price = (await crypto_price.simple_price(ids=id_coin, vs_currestring="rub"))[id_coin]["rub"]
        input_content = InputTextMessageContent(
            lazy_gettext("""название {name}\n`стоимость 1 {name} - {valvue}₽`\nдата {date} """
                         ).format(name=text, valvue=price, date=bankapi.date)
            )
        item = InlineQueryResultArticle(
            id=result_id,
            title=lazy_gettext('{name} - {price}').format(name=text, price=price),
            input_message_content=input_content
        )
    elif text == "rub":
        id_coin = crypto["btc"]["id"]
        price = (await crypto_price.simple_price(ids=id_coin, vs_currestring="rub"))[id_coin]["rub"]
        input_content = InputTextMessageContent(
            lazy_gettext("""название {name}\n`стоимость 1 {name}:\n{btc} btc\n$ {usd} `\nдата {date} """
                         ).format(name=text, btc=(1 / price), usd=(1 / res["USD"]["valvue"]), date=bankapi.date)
        )
        item = InlineQueryResultArticle(
            id=result_id,
            title=lazy_gettext('{name}:{price} btc ').format(name=text, price=(1 / price)),
            input_message_content=input_content
        )



    else:

        input_content = InputTextMessageContent(
            lazy_gettext("нет такой валюты\nдоступные={name}").format(name=list(res.keys())))
        result_id: str = hashlib.md5(text.encode()).hexdigest()
        item = InlineQueryResultArticle(
            id=result_id,
            title=lazy_gettext("нет такой валюты"),
            input_message_content=input_content
        )

    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)