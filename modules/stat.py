import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from aioinflux import InfluxDBClient, InfluxDBWriteError


@dataclass
class EvnDB:
    STATS_DB: str
    STATS_HOST: str
    STATS_USER: str
    STATS_PASS: str


class Command(Enum):
    START = "/start"
    RESTART = "/restart"
    STOP = "/stop"
    PING = "/ping"
    HELP = "/help"


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
        async with InfluxDBClient(host=DBParams.STATS_HOST, db=DBParams.STATS_DB,
                                  username=DBParams.STATS_USER, password=DBParams.STATS_PASS) as client:
            await client.write(data)
    except InfluxDBWriteError as ex:
        logging.error(f"InfluxDB write error: {str(ex)}")

