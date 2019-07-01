# This Python file uses the following encoding: utf-8

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton


class button:
    def button_all(text_button: str, callback: str) -> InlineKeyboardMarkup:
        inline_btn_1 = InlineKeyboardButton(text=text_button, callback_data=callback)
        inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
        return inline_kb1

    def proxy(list_proxy: list) -> InlineKeyboardMarkup:
        inline_kb1 = InlineKeyboardMarkup()
        for i in list_proxy:
            s: str = i.replace("socks5://", "")
            server, port = s.split(":")
            link_beta: str = f"https://t.me/proxy?server={server}&port={port}"
            inline_kb1.add(InlineKeyboardButton(server, url=link_beta))
        return inline_kb1


class keyboard:
    # resize_keyboard=True, one_time_keyboard=True
    def keyboard_all(text: str) -> ReplyKeyboardMarkup:
        button_hi = KeyboardButton(text=text)
        greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        greet_kb.add(button_hi)
        return greet_kb

    @staticmethod
    def remove_kaeyboard() -> ReplyKeyboardRemove:
        """

        
        :param kwargs: 
        :return: 
        """
        return ReplyKeyboardRemove()

    def get_contact(text_contact: str) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text=text_contact, request_contact=True))

    def geotag(text_geo: str) -> ReplyKeyboardMarkup:
        
        return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text=text_geo, request_location=True))


