# This Python file uses the following encoding: utf-8

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton


class button:
    @staticmethod
    def start() -> InlineKeyboardMarkup:
        inline_btn_1 = InlineKeyboardButton('Первая кнопка', callback_data='button')
        inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
        return inline_kb1
    @staticmethod
    def proxy(list_proxy:list) -> InlineKeyboardMarkup:
        inline_kb1 = InlineKeyboardMarkup()
        for i in list_proxy:
           s:str= i.replace("socks5://", "")
           server,port =s.split(":")
           link_beta: str = f"https://t.me/proxy?server={server}&port={port}"
           inline_kb1.add(InlineKeyboardButton(server, url=link_beta))
        inline_btn_1 = InlineKeyboardButton('Первая кнопка',callback_data='button')
        inline_kb1.add(inline_btn_1)
        return inline_kb1



class keyboard:
    #resize_keyboard=True, one_time_keyboard=True
    @staticmethod
    def start(*args:str) -> ReplyKeyboardMarkup:
        button_hi = KeyboardButton(args)
        greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        greet_kb.add(button_hi)
        return greet_kb

    @staticmethod
    def remove() -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove()

    @staticmethod
    def get_contact()-> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить свой контакт ', request_contact=True))


