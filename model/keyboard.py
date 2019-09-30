# This Python file uses the following encoding: utf-8

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from typing import List


class Keyboard:
    # resize_keyboard=True, one_time_keyboard=True
    @staticmethod
    def keyboard_all(text: str) -> ReplyKeyboardMarkup:
        """

        :param text:
        :return:
        """
        button_hi = KeyboardButton(text=text)
        greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        greet_kb.add(button_hi)
        return greet_kb

    @staticmethod
    def remove_keyboard() -> ReplyKeyboardRemove:
        """


        :return:
        """
        return ReplyKeyboardRemove()

    @staticmethod
    def get_contact(text_contact: str) -> ReplyKeyboardMarkup:
        """

        :param text_contact:
        :return:
        """
        return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text=text_contact, request_contact=True),
                                                             one_time_keyboard=True)

    @staticmethod
    def geo_tag(text_geo: str) -> ReplyKeyboardMarkup:
        """

        :param text_geo:
        :return:
        """
        return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text=text_geo, request_location=True),
                                                             one_time_keyboard=True)

    @staticmethod
    def get_lang(lang: List[str]) -> ReplyKeyboardMarkup:
        """

        :param lang:
        :return:
        """
        return ReplyKeyboardMarkup([[KeyboardButton(text=item)] for item in lang], resize_keyboard=True)
