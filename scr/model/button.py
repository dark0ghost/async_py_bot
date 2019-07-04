# This Python file uses the following encoding: utf-8

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from typing import List


class Button:
    posts_cb: CallbackData = CallbackData('post', 'id', 'action')

    @classmethod
    def button_all(cls, text_button: str, callback: str) -> InlineKeyboardMarkup:
        inline_btn = InlineKeyboardButton(text=text_button,
                                          callback_data=cls.posts_cb.new(id=callback, action=text_button))
        inline_kb = InlineKeyboardMarkup().add(inline_btn)
        return inline_kb

    def proxy(list_proxy: List[str]) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup()
        for i in list_proxy:
            s: str = i.replace("socks5://", "")
            server, port = s.split(":")
            link_beta: str = f"https://t.me/proxy?server={server}&port={port}"
            inline_kb.add(InlineKeyboardButton(server, url=link_beta))
        return inline_kb

    @classmethod
    def butoons(cls, text: List[str], call_back: list) -> InlineKeyboardMarkup:
        inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
        for val, i in enumerate(text):
            inb = InlineKeyboardButton(text=i, callback_data=cls.posts_cb.new(id=call_back[i]))
            inline_kb.add(inb)
        return inline_kb

    @classmethod
    def edit_proxy(cls, text_button: str, proxy: str, callback: str = "proxy") -> InlineKeyboardMarkup:
        proxy = proxy.replace("socks5://", "")
        server, port = proxy.split(":")
        inline_btn = InlineKeyboardButton(text=text_button,
                                          callback_data=Button.posts_cb.new(id=callback, action=text_button))
        link_beta: str = f"https://t.me/proxy?server={server}&port={port}"
        inline_kb = InlineKeyboardMarkup()
        inline_kb.add(InlineKeyboardButton(text="proxy for you", url=link_beta))
        inline_kb.add(inline_btn)
        return inline_kb
