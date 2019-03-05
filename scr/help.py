import os
from aiogram.utils.helper import Helper, HelperMode, ListItem

package = ["aiodns", "aiohttp", "async-timeout", "beautifulsoup4", "aiogram", "aiosqlite", "aiosocks", "aiosocksy",
           "aiohttp_socks"]

token = " "


mes = {
    "start": "message start",
    "help":"message help",

}

class st(Helper):
    mode = HelperMode.snake_case
    TEST_STATE_0 = ListItem()
    TEST_STATE_1 = ListItem()
    TEST_STATE_2 = ListItem()
    TEST_STATE_3 = ListItem()
    TEST_STATE_4 = ListItem()
    TEST_STATE_5 = ListItem()
