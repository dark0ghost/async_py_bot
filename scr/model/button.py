# This Python file uses the following encoding: utf-8

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton


class button:
    @staticmethod
    def start() -> InlineKeyboardMarkup:
        inline_btn_1 = InlineKeyboardButton('Первая кнопка', callback_data='button')
        inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
        return inline_kb1


class keyboard:
    #resize_keyboard=True, one_time_keyboard=True
    @staticmethod
    def start(*args) -> ReplyKeyboardMarkup:
        button_hi = KeyboardButton('Привет! ')
        greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        greet_kb.add(button_hi)
        return greet_kb

    @staticmethod
    def remove():
        return ReplyKeyboardRemove()

    @staticmethod
    def get_contact():
        return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить свой контакт ', request_contact=True))


