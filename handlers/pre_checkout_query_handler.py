# This Python file uses the following encoding: utf-8
from main import bot,dp
from aiogram import types
import help


@dp.pre_checkout_query_handler()
async def checkout(pre_checkout_query: types.PreCheckoutQuery):

    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=1,
                                        error_message=help.mes["error_pay"])