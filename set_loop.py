from asyncio import AbstractEventLoop

import asyncio

loop: AbstractEventLoop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
