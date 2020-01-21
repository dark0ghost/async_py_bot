from abc import ABC

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
import helps


class Base_bot_filter(BoundFilter):
    key = 'is_master'

    def __init__(self, is_admin=False):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        pass


class MasterFilter(BoundFilter):
    key = 'is_master'

    def __init__(self, is_admin=False):
        self.is_admin = is_admin

    def check(self, message: types.Message):
        return message.chat.id == helps.master
