from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

class Base_bot_filter(BoundFilter):
    key = ' '

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
           pass