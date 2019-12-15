from asyncio import AbstractEventLoop

import asyncio

"""
fix :
RuntimeError: There is no current event loop in thread 'MainThread'.
"""
loop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(loop=loop)
