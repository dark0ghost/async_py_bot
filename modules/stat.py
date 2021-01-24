import logging
import os
from datetime import datetime
from enum import Enum

from aioinflux import InfluxDBClient, InfluxDBWriteError


class EvnDB:
    STATS_DB: str = os.environ.get("STATS_DB")
    STATS_HOST: str = os.environ.get("STATS_HOST")
    STATS_USER: str = os.environ.get("STATS_USER")
    STATS_PASS: str = os.environ.get("STATS_PASS")


class Command(Enum):
    START = "/start"
    RESTART = "/restart"
    STOP = "/stop"
    PING = "/ping"
    HELP = "/help"
    JSONBOX = "jsonbox"
    PASTEBIN = "pastebin"
    LANGUAGE='language'


async def detect(id_user: int, command: Command):
    data = {
        "measurement": "bot_commands",
        "time": datetime.now(),
        "fields": {"event": 1},
        "tags": {
            "user": str(id_user),
            "command": command.value
        }
    }
    try:
        async with InfluxDBClient(host=EvnDB.STATS_HOST, db=EvnDB.STATS_DB,
                                  username=EvnDB.STATS_USER, password=EvnDB.STATS_PASS) as client:
            await client.write(data)
    except InfluxDBWriteError as e:
        logging.error(f"InfluxDB write error: {e}")
