# This Python file uses the following encoding: utf-8
import hashlib
from typing import List

from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

from core import dp, bot, lazy_get_text, cb as bank_api, crypto_price, Button


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery) -> InlineQueryResultArticle:
    """
    :param inline_query:
    :return:
    """
    text = inline_query.query
    res = await bank_api.build_list_coin()
    crypto = await crypto_price.coin_list()
    result_id: str = hashlib.sha256(text.encode()).hexdigest()
    result_list: List[InlineQueryResultArticle] = []
    if text in res.keys():
        input_content = InputTextMessageContent(lazy_get_text(
            """название {name} 
        стоимость  {name}  {valvue}₽
        дата {date}
         """).format(name=text, valvue=res[text]["valvue"],
                                                                date=bank_api.date))

        item = InlineQueryResultArticle(
            id=result_id,
            title=lazy_get_text('{name}  {valvue}').format(name=text, valvue=res[text]["valvue"]),
            input_message_content=input_content
        )
    elif text in crypto:
        id_coin = crypto[text]["id"]
        price = (await crypto_price.simple_price(ids=id_coin, vs_currestring="rub"))[id_coin]["rub"]
        input_content = InputTextMessageContent(
            lazy_get_text("""название {name}\nстоимость {name}  {valvue}₽\nдата {date} """
                          ).format(name=text, valvue=price, date=bank_api.date)
        )
        item = InlineQueryResultArticle(
            id=result_id,
            title=lazy_get_text('{name}  {price}').format(name=text, price=price),
            input_message_content=input_content
        )
    elif text == "rub":
        id_coin = crypto["btc"]["id"]
        price = (await crypto_price.simple_price(ids=id_coin, vs_currestring="rub"))[id_coin]["rub"]
        input_content = InputTextMessageContent(
            lazy_get_text("""название {name}\nстоимость 1 {name} \n{btc} btc\n$ {usd} \nдата {date} """
                          ).format(name=text, btc=(1 / price), usd=(1 / res["USD"]["valvue"]), date=bank_api.date)
        )
        item = InlineQueryResultArticle(
            id=result_id,
            title=lazy_get_text('{name} {price} btc ').format(name=text, price=(1 / price)),
            input_message_content=input_content
        )
    else:
        input_content = InputTextMessageContent(
            lazy_get_text("нет такой валюты\nдоступные {name}").format(name=list(res.keys())))
        result_id: str = hashlib.md5(text.encode()).hexdigest()
        item = InlineQueryResultArticle(
            id=result_id,
            title=lazy_get_text("нет такой валюты"),
            input_message_content=input_content
        )
    result_list.append(item)
    return await bot.answer_inline_query(inline_query.id, results=result_list, cache_time=1)
