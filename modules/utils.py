import contextvars
import functools
from concurrent.futures.thread import ThreadPoolExecutor

from aiogram.utils.callback_data import CallbackData

import uvloop

loop = uvloop.new_event_loop()

_executor = ThreadPoolExecutor()

reaction_cd = CallbackData('rctn', 'r')
settings_cd = CallbackData('settings', 'set')
lang_cd = CallbackData('lang', 'lang')
page_cd = CallbackData('page', 'page')
word_cd = CallbackData('word', 'word')


def aiowrap(func):
    @functools.wraps(func)
    def wrapping(*args, **kwargs):
        new_func = functools.partial(func, *args, **kwargs)
        ctx = contextvars.copy_context()
        ctx_func = functools.partial(ctx.run, new_func)
        return loop.run_in_executor(_executor, ctx_func)
    return wrapping