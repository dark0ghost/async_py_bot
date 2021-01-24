import os

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class MasterFilter(BoundFilter):
    key = 'is_master'

    def __init__(self, is_admin=False):
        self.is_admin = is_admin
        self.master = os.environ.get("MASTER")

    def check(self, message: types.Message):
        return message.chat.id == self.master


