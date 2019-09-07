# This Python file uses the following encoding: utf-8

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from typing import List


class Button:

    def __init__(self):
        self.posts_cb: CallbackData = CallbackData('post', 'id', 'action')

    def __del__(self):
        del self.posts_cb

    def button_all(self, text_button: str, callback: str) -> InlineKeyboardMarkup:
        """

        :param text_button:
        :param callback:
        :return:
        """
        inline_btn = InlineKeyboardButton(text=text_button,
                                          callback_data=self.posts_cb.new(id=callback, action=text_button),row_width=3)
        inline_kb = InlineKeyboardMarkup().add(inline_btn)
        return inline_kb

    def proxy(list_proxy: List[str]) -> InlineKeyboardMarkup:
        """

        :return:
        """
        inline_kb = InlineKeyboardMarkup()
        for i in list_proxy:
            s: str = i.replace("socks5://", "")
            server, port = s.split(":")
            link_beta: str = f"https://t.me/proxy?server={server}&port={port}"
            inline_kb.add(InlineKeyboardButton(server, url=link_beta))
        return inline_kb

    def buttons(self, text: List[str], call_back: List[str]) -> InlineKeyboardMarkup:
        """

        :param text:
        :param call_back:
        :return:
        """
        inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
        for val, i in enumerate(text):
            inb = InlineKeyboardButton(text=i,
                                       callback_data=self.posts_cb.new(id=hash(call_back[val]), action=call_back[val]),)
            inline_kb.insert(inb)
        return inline_kb

    def edit_proxy(self, text_button: str, proxy: str, callback: str = "proxy") -> InlineKeyboardMarkup:
        """

        :param text_button:
        :param proxy:
        :param callback:
        :return:
        """
        proxy = proxy.replace("socks5://", "")
        server, port = proxy.split(":")
        inline_btn = InlineKeyboardButton(text=text_button,
                                          callback_data=self.posts_cb.new(id=callback, action=callback))
        link_beta: str = f"https://t.me/proxy?server={server}&port={port}"
        inline_kb = InlineKeyboardMarkup()
        inline_kb.add(InlineKeyboardButton(text=server, url=link_beta))
        inline_kb.add(inline_btn)
        return inline_kb
