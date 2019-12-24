import aiohttp
import typing
import datetime
import asyncio

from aiohttp_socks import SocksConnector


class Etherscan:
    delay: int = 5
    time_delay: int = 1
    now: datetime.datetime = datetime.datetime.now()
    action_balance: str = "balance"
    action_balancemulti: str = "balancemulti"
    action_txlist: str = "txlist"
    action_txlistinternal: str = "txlistinternal"
    action_tokentx: str = "tokentx"
    action_getminedblock: str = "getminedblock"

    def __init__(self, api_key: str, session: typing.Optional[aiohttp.ClientSession] = None) -> None:
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

    async def eth_blockNumber(self) -> typing.Dict[str, str]:
        """
        Returns the number of most recent block
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey={self.api}") as respsonse:
            return await respsonse.json()

    async def eth_getBlockByNumber(self, block: str) -> typing.Dict[str, str]:
        """
        Returns information about a block by block number
        @param block:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag={block}f&boolean=true&apikey={self.api}") as response:
            return await response.json()

    async def eth_getUncleByBlockNumberAndIndex(self, block: str) -> typing.Dict[str, str]:
        """
        Returns information about a uncle by block number
        @param block:
        @return:
        """
        async with self.session.get(f"https://api.etherscan.io/api?module=proxy&action"
                                    f"=eth_getUncleByBlockNumberAndIndex&tag={block}&index=0x0&apikey={self.api}") as \
                response:
            return await response.json()

    async def eth_getBlockTransactionCountByNumber(self, block: str) -> typing.Dict[str, str]:
        """
        Returns the number of transactions in a block from a block matching the given block number
        @param block:
        @return:
        """
        async with self.session.get(f"https://api.etherscan.io/api?module=proxy&action"
                                    f"=eth_getBlockTransactionCountByNumber&tag={block}&apikey={self.api}") as \
                response:
            return await response.json()

    async def eth_getTransactionByHash(self, hash: str) -> typing.Dict[str, str]:
        """
        Returns the information about a transaction requested by transaction hash
        @param hash:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={hash}&apikey={self.api}") as response:
            return await response.json()

    async def eth_getTransactionByBlockNumberAndIndex(self, block: str) -> typing.Dict[str, str]:
        """
        Returns information about a transaction by block number and transaction index position
        @param block:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByBlockNumberAndIndex&tag"
                f"={block}f&index=0x0&apikey={self.api}") as response:
            return await response.json()

    async def eth_getTransactionCount(self, address: str) -> typing.Dict[str, str]:
        """
        Returns the number of transactions sent from an address
        @param address:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionCount&address={address}&tag=latest&apikey={self.api}") as response:
            return await response.json()

    async def eth_sendRawTransaction(self, hex_: str) -> typing.Dict[str, str]:
        """
        Creates new message call transaction or a contract creation for signed transactions
        @param hex_:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_sendRawTransaction&hex={hex_}&apikey={self.api}") as response:
            return await response.json()

    async def eth_getTransactionReceipt(self, hash: str) -> typing.Dict[str, str]:
        """
        Returns the receipt of a transaction by transaction hash
        @param hash:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash={hash}&apikey={self.api}") as response:
            return await response.json()

    async def eth_call(self, to: str, data: str) -> typing.Dict[str, str]:
        """
        Executes a new message call immediately without creating a transaction on the block chain
        @param to:
        @param data:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_call&to={to}&data={data}&tag=latest&apikey={self.api}") as response:
            return await response.json()

    async def eth_getCode(self, address: str) -> typing.Dict[str, str]:
        """
        Returns code at a given address
        @param address:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getCode&address={address}&tag=latest&apikey={self.api}") as response:
            return await response.json()

    async def eth_getStorageAt(self, address: str) -> typing.Dict[str, str]:
        """
        (**experimental)
        Returns the value from a storage position at a given address
        @param address:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getStorageAt&address={address}&position=0x0&tag=latest&apikey={self.api}") as response:
            return await response.json()

    async def eth_gasPrice(self) -> typing.Dict[str, str]:
        """
        Returns the current price per gas in wei
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_gasPrice&apikey={self.api}") as response:
            return await response.json()

    async def eth_estimateGas(self, to: str, gasprice: str, gas: int, valvue: int = 0xff22) -> typing.Dict[str, str]:
        """
        Makes a call or transaction, which won't be added to the blockchain and returns the used gas, which can be used for estimating the used gas
        @param gas:
        @param valvue:
        @param gasprice:
        @param to:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_estimateGas&to=&value={valvue}&gasPrice={gasprice}&gas={gas}&apikey={self.api}") as response:
            return await response.json()


import asyncio


async def main():
    f = Etherscan(api_key="KK8G6CQ1XG8NT2P5KTVVNUWTB98SCMCZ8Q")
    await f.open_session()

    print(await f.eth_blockNumber())
    print(await f.eth_getBlockByNumber("0x9d4f"))
    print(await f.eth_getTransactionByBlockNumberAndIndex("0x9d4f"))
    print(await f.eth_getBlockTransactionCountByNumber("0x9d4f"))
    print(await f.eth_getTransactionByHash("0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1"))
    print(await f.eth_getUncleByBlockNumberAndIndex("0x10d4f"))
    print(await f.eth_getTransactionCount("0x2910543af39aba0cd09dbb2d50200b3e800a63d2"))
    print(await f.eth_sendRawTransaction("0xf904808000831cfde080"))
    print(await f.eth_getTransactionReceipt("0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1"))
    print(await f.eth_call(to="0xAEEF46DB4855E25702F8237E8f403FddcaF931C0",
                           data="0x70a08231000000000000000000000000e16359506c028e51f16be38986ec5746251e9724"))
    print(await f.eth_getBlockByNumber("0xf75e354c5edc8efed9b59ee9f67a80845ade7d0c"))
    print(await f.eth_getStorageAt("0x6e03d9cce9d60f3e9f2597e13cd4c54c55d3e433"))
    print(await f.eth_gasPrice())
    print(
        await f.eth_estimateGas(to="0xf0160428a8552ac9bb7e050d90eeade4ddd52843", gasprice="0x051da038cc", gas=0xffffff))

    await f.close()


asyncio.run(main())
