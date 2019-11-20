import contextvars
import functools
from asyncio import AbstractEventLoop
from concurrent.futures.thread import ThreadPoolExecutor

import asyncio
from aiogram.utils.callback_data import CallbackData

import uvloop
from typing import Callable

from set_loop import loop

_executor = ThreadPoolExecutor()

reaction_cd = CallbackData('rctn', 'r')
settings_cd = CallbackData('settings', 'set')
lang_cd = CallbackData('lang', 'lang')
page_cd = CallbackData('page', 'page')
word_cd = CallbackData('word', 'word')


def g(name):
    print(name)
    return name


def aiowrap(func: Callable) -> object:
    @functools.wraps(func)
    def wrapping(*args, **kwargs):
        new_func = functools.partial(func, *args, **kwargs)
        ctx = contextvars.copy_context()
        ctx_func = functools.partial(ctx.run, new_func)
        return loop.run_in_executor(_executor, ctx_func)

    return wrapping


class Aiowrap:
    def __init__(self, loop: AbstractEventLoop) -> None:
        self.loop = loop

    def __call__(self, func: Callable, *args, **kwargs) -> AbstractEventLoop:
        @functools.wraps(func)
        def wrapping(_executor=None, *args, **kwargs):
            new_func = functools.partial(func, *args, **kwargs)
            ctx = contextvars.copy_context()
            ctx_func = functools.partial(ctx.run, new_func)
            return loop.run_in_executor(_executor, ctx_func)

        return wrapping
