# This Python file uses the following encoding: utf-8

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from typing import List


class Keyboard:
    # resize_keyboard=True, one_time_keyboard=True
    def keyboard_all(text: str) -> ReplyKeyboardMarkup:
        button_hi = KeyboardButton(text=text)
        greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        greet_kb.add(button_hi)
        return greet_kb

    def remove_kaeyboard(*args) -> ReplyKeyboardRemove:
        """


        :param kwargs:
        :return:
        """
        return ReplyKeyboardRemove()

    def get_contact(text_contact: str) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text=text_contact, request_contact=True),
                                                             one_time_keyboard=True)

    def geotag(text_geo: str) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text=text_geo, request_location=True),
                                                             one_time_keyboard=True)

    def get_lang(lang: List[str]):
        print(lang)
        return ReplyKeyboardMarkup([[KeyboardButton(text=item)] for item in lang], resize_keyboard=True)
