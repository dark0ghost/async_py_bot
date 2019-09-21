from main import dp, loop, shutdown
from aiogram import executor
import handlers.message_handler
import handlers.pre_checkout_query_handler
import handlers.callback_handlers
import handlers.inline_handlers
import handlers.shoping_handler
from model.auth import Auth





if __name__ == '__main__':
    print("start")
    executor.start_polling(dp, on_shutdown=shutdown, loop=loop)
