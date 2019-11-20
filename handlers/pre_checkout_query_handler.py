# This Python file uses the following encoding: utf-8
from core import bot,dp
from aiogram import types
import helps


@dp.pre_checkout_query_handler()
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    """
    todo : check trans
    :param pre_checkout_query:
    :return:
    """

    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=1,
                                        error_message=helps.mes["error_pay"])