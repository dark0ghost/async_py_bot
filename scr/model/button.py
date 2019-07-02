# This Python file uses the following encoding: utf-8

from aiogram.types import InlineKeyboardMarkup,  InlineKeyboardButton

class button:
    def button_all(text_button: str, callback: str) -> InlineKeyboardMarkup:
        inline_btn = InlineKeyboardButton(text=text_button, callback_data=callback)
        inline_kb = InlineKeyboardMarkup().add(inline_btn)
        return inline_kb

    def proxy(list_proxy: list) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup()
        for i in list_proxy:
            s: str = i.replace("socks5://", "")
            server, port = s.split(":")
            link_beta: str = f"https://t.me/proxy?server={server}&port={port}"
            inline_kb.add(InlineKeyboardButton(server, url=link_beta))
        return inline_kb

    def butoons(text: list, call_back: list)-> InlineKeyboardMarkup:
        inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup()
        for val, i in enumerate(text):
            inb = InlineKeyboardButton(text=i, callback_data=call_back[i])
            inline_kb.add(inb)
        return inline_kb