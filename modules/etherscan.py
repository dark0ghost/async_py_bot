import aiohttp
import typing
import datetime
import asyncio

from aiohttp_socks import SocksConnector


class Etherscan:
    delay: int = 5
    time_delay: int = 1
    now: datetime.datetime = datetime.datetime.now()
    account_api: str = "https://api.etherscan.io/api?module=account&action={action}&address={address}&tag={" \
                       "teg}t&apikey={apikey} "
    action_balance: str = "balance"
    action_balancemulti: str = "balancemulti"
    action_txlist: str = "txlist"
    action_txlistinternal: str = "txlistinternal"
    action_tokentx: str = "tokentx"
    action_getminedblock: str = "getminedblock"

    def __init__(self, api_key: str, session: typing.Optional[aiohttp.ClientSession] = None):
        """

        @param api_key:
        @param session:
        """

        self.session = session
        self.api: str = api_key

    def is_limit_time(self) -> bool:
        """

        @rtype: object
        """
        then = datetime.datetime.now()
        delta = self.now - then
        return delta.seconds > 1

    async def open_session(self, proxy: typing.Optional[str] = None) -> aiohttp.ClientSession:
        """

        @type proxy: object
        """
        if proxy is None:
            self.session = aiohttp.ClientSession()
            return self.session
        connector = SocksConnector.from_url(proxy)
        self.session = aiohttp.ClientSession(connector=connector)
        return self.session

    async def close(self) -> None:
        """

        @return:
        """
        await self.session.close()
        return
