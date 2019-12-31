import aiohttp
import typing
import datetime

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

    class BadRequest(Exception):
        pass

    def __init__(self, api_key: str, session: typing.Optional[aiohttp.ClientSession] = None) -> None:
        """

        @param api_key:
        @param session:
        """

        self.session = session
        self.api: str = api_key

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.api})"

    def __hash__(self) -> int:
        return hash(self.api + self.__str__())

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

    async def eth_blockNumber(self) -> typing.Dict[str, typing.Any]:
        """
        Returns the number of most recent block
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey={self.api}") as respsonse:
            return await respsonse.json()

    async def eth_getBlockByNumber(self, block: str) -> typing.Dict[str, typing.Any]:
        """
        Returns information about a block by block number
        @param block:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag={block}f&boolean=true&apikey={self.api}") as response:
            return await response.json()

    async def eth_getUncleByBlockNumberAndIndex(self, block: str) -> typing.Dict[str, typing.Any]:
        """
        Returns information about a uncle by block number
        @param block:
        @return:
        """
        async with self.session.get(f"https://api.etherscan.io/api?module=proxy&action"
                                    f"=eth_getUncleByBlockNumberAndIndex&tag={block}&index=0x0&apikey={self.api}") as \
                response:
            return await response.json()

    async def eth_getBlockTransactionCountByNumber(self, block: str) -> typing.Dict[str, typing.Any]:
        """
        Returns the number of transactions in a block from a block matching the given block number
        @param block:
        @return:
        """
        async with self.session.get(f"https://api.etherscan.io/api?module=proxy&action"
                                    f"=eth_getBlockTransactionCountByNumber&tag={block}&apikey={self.api}") as \
                response:
            return await response.json()

    async def eth_getTransactionByHash(self, hash: str) -> typing.Dict[str, typing.Any]:
        """
        Returns the information about a transaction requested by transaction hash
        @param hash:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={hash}&apikey={self.api}") as response:
            return await response.json()

    async def eth_getTransactionByBlockNumberAndIndex(self, block: str) -> typing.Dict[str, typing.Any]:
        """
        Returns information about a transaction by block number and transaction index position
        @param block:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByBlockNumberAndIndex&tag"
                f"={block}f&index=0x0&apikey={self.api}") as response:
            return await response.json()

    async def eth_getTransactionCount(self, address: str) -> typing.Dict[str, typing.Any]:
        """
        Returns the number of transactions sent from an address
        @param address:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionCount&address={address}&tag=latest&apikey={self.api}") as response:
            return await response.json()

    async def eth_sendRawTransaction(self, hex_: str) -> typing.Dict[str, typing.Any]:
        """
        Creates new message call transaction or a contract creation for signed transactions
        @param hex_:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_sendRawTransaction&hex={hex_}&apikey={self.api}") as response:
            return await response.json()

    async def eth_getTransactionReceipt(self, __hash: str) -> typing.Dict[str, typing.Any]:
        """
        Returns the receipt of a transaction by transaction hash
        @param __hash:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash={__hash}&apikey={self.api}") as response:
            return await response.json()

    async def eth_call(self, to: str, data: str) -> typing.Dict[str, typing.Any]:
        """
        Executes a new message call immediately without creating a transaction on the block chain
        @param to:
        @param data:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_call&to={to}&data={data}&tag=latest&apikey={self.api}") as response:
            return await response.json()

    async def eth_getCode(self, address: str) -> typing.Dict[str, typing.Any]:
        """
        Returns code at a given address
        @param address:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getCode&address={address}&tag=latest&apikey={self.api}") as response:
            return await response.json()

    async def eth_getStorageAt(self, address: str) -> typing.Dict[str, typing.Any]:
        """
        (**experimental)
        Returns the value from a storage position at a given address
        @param address:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_getStorageAt&address={address}&position=0x0&tag=latest&apikey={self.api}") as response:
            return await response.json()

    async def eth_gasPrice(self) -> typing.Dict[str, typing.Any]:
        """
        Returns the current price per gas in wei
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=proxy&action=eth_gasPrice&apikey={self.api}") as response:
            return await response.json()

    async def eth_estimateGas(self, to: str, gasprice: str, gas: int, valvue: int = 0xff22) -> typing.Dict[
        str, typing.Any]:
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

    async def ether_balance_single_address(self, address: str) -> typing.Dict[str, typing.Any]:
        """
        Get Ether Balance for a single Address
        @param address:
        @return:
        """
        async with self.session.get(f"https://api.etherscan.io/api?module=account&action=balance&address={address}"
                                    f"&tag=latest&&apikey={self.api}") as response:
            return await response.json()

    async def ether_balance_multiple_addresses(self, list_adders: typing.List[str]) -> \
            typing.Dict[str, typing.Any]:
        """
        Get Ether Balance for multiple Addresses in a single call
        Separate addresses by comma, up to a maxium of 20 accounts in a single batch
        @param list_adders:
        @return:
        """
        if len(list_adders) <= 20:
            data: str = ",".join(list_adders)
            async with self.session.get(
                    f"https://api.etherscan.io/api?module=account&action=balancemulti&address={data}&tag=latest&apikey={self.api}") as response:
                return await response.json()
        await self.session.close()
        raise self.BadRequest("max len 20")

    async def list_of_normal_transactions(self, address: str, start_block: int = 0, end_block: int = 99999999,
                                          offset: typing.Optional[int] = None) -> \
            typing.Dict[str, typing.Any]:
        """
        Get a list of 'Normal' Transactions By Address [Optional Parameters] startblock: starting blockNo to retrieve
        results, endblock: ending blockNo to retrieve results
        (Returned 'isError' values: 0=No Error, 1=Got Error)
        (Returns up to a maximum of the last 10000 transactions only)
        or
        (To get paginated results use offset=<max records to return>)


        @param offset:
        @param end_block:
        @param start_block:
        @param address:
        @return:
        """
        if offset is None:
            async with self.session.get(
                    f"http://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={start_block}&endblock={end_block}&sort=asc&apikey={self.api}") as response:
                return await response.json()
        async with self.session.get(
                f"http://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={start_block}&endblock={end_block}&sort=asc&apikey={self.api}&offset={offset}") as response:
            return await response.json()

    async def list_of_internal_transactions_by_address(self, address: str, start_block: int = 0,
                                                       end_block: int = 2702578,
                                                       offset: typing.Optional[int] = None, page: int = 1) -> \
            typing.Dict[str, typing.Any]:
        """
        [Optional Parameters] startblock: starting blockNo to retrieve results, endblock: ending blockNo to retrieve results
        (Returned 'isError' values: 0=No Error, 1=Got Error)
        (Returns up to a maximum of the last 10000 transactions only)
        or
        (To get paginated results use page=<page number> and offset=<max records to return>)

        @param address:
        @param start_block:
        @param end_block:
        @param offset:
        @param page:
        @return:
        """

        if offset is None:
            async with self.session.get(
                    f"http://api.etherscan.io/api?module=account&action=txlistinternal&address={address}3&startblock={start_block}&endblock={end_block}&sort=asc&apikey={self.api}") as response:
                return await response.json()
        async with self.session.get(
                f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={address}&startblock={start_block}&endblock={end_block}&page={page}&offset={offset}&sort=asc&apikey={self.api}") as response:
            return await response.json()

    async def internal_transactions_by_transaction_hash(self, __hash: str) -> typing.Dict[str, typing.Any]:
        """
        (Returned 'isError' values: 0=Ok, 1=Rejected/Cancelled)
        (Returns up to a maximum of the last 10000 transactions only)
        @param __hash:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=account&action=txlistinternal&txhash={__hash}&apikey={self.api}") as response:
            return await response.json()

    async def list_of_ERC20_token_transfer_events__by_address(self) -> typing.Dict[str, typing.Any]:
        pass


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
    print(await f.ether_balance_single_address("0x2a6e46570566659dd87939e20f0857b26c966749"))
    print(await f.ether_balance_multiple_addresses(["0xAEEF46DB4855E25702F8237E8f403FddcaF931C0",
                                                    "0x2a6e46570566659dd87939e20f0857b26c966749"]))
    print(await f.list_of_normal_transactions("0x2A6E45970566659DD87939E20f0857B26c966749"))
    print(await f.list_of_normal_transactions("0x2A6E45970566659DD87939E20f0857B26c966749"))
    print(await f.list_of_normal_transactions("0x2A6E45970566659DD87939E20f0857B26c966749", 10))
    print(await f.list_of_internal_transactions_by_address("0x2A6E45970566659DD87939E20f0857B26c966749"))
    print(await f.list_of_internal_transactions_by_address("0x2A6E45970566659DD87939E20f0857B26c966749", 10))
    print(await f.internal_transactions_by_transaction_hash(
        "0x40eb908387324f2b575b4879cd9d7188f69c8fc9d87c901b9e2daaea4b442170"))
    print(hash(f))
    print(f)

    await f.close()


asyncio.run(main())
