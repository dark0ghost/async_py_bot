# This Python file uses the following encoding: utf-8
from core import dp, bot
from aiogram import types

import price


@dp.shipping_query_handler()
async def shipping(shipping_query: types.ShippingQuery):
    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=price.shipping_options,
                                    error_message=f'доставка не работает!')
