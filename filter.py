from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class Base_bot_filter(BoundFilter):
    key = ' '

    def __init__(self, is_admin=False):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        pass


def is_master(message: types.Message):
    return message.chat.id == 387544140
