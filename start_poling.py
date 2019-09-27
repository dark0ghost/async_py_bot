from main import dp, loop, shutdown
from aiogram import executor
import importlib

importlib.import_module('handlers.message_handler')
importlib.import_module('handlers.pre_checkout_query_handler')
importlib.import_module('handlers.callback_handlers')
importlib.import_module('handlers.inline_handlers')
importlib.import_module('handlers.shoping_handler')


if __name__ == '__main__':
    print("start")
    executor.start_polling(dp, on_shutdown=shutdown, loop=loop)
