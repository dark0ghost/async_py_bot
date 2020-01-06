import aiohttp
import typing
import datetime

from aiohttp_socks import SocksConnector


class Etherscan:
    """
    @see
    DOC FOR USE :
     async def main():
       f = Etherscan(api_key="{token}")
        await f.open_session() # or Etherscan(api_key="{token}",session)
        print(await f.your_method())
     asyncio.run(main())
    """

    class BadRequest(Exception):
        """
        @doc
        class for custom exception
        """
        pass

    def __init__(self, api_key: str, session: typing.Optional[aiohttp.ClientSession] = None) -> None:
        """
        @param api_key:
        @param session:
        """

        self.session = session
        self.api: str = api_key

    def __str__(self) -> str:
        """

        @return:
        """
        return f"{self.__class__.__name__}({self.api})"

    def __hash__(self) -> int:
        """

        @return:
        """
        return hash(self.api + self.__str__())

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
        close session
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

    async def eth_estimateGas(self, to: str, gasprice: str, gas: int, valvue: int = 0xff22) -> \
            typing.Dict[str, typing.Any]:
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

    async def contract_abi_for_verified_contract_source_codes(self, address: str) -> typing.Dict[str, typing.Any]:
        """
        Get Contract ABI for Verified Contract Source Codes
        @param address:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={self.api}") as response:
            return await response.json()

    async def get_source_code_contract(self, address: str) -> typing.Dict[str, typing.Any]:
        """

        @param address:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={self.api}") as response:
            return await response.json()

    async def check_source_code_verification_submission_status(self, guid: str, module: str = "contract",
                                                               action: str = "checkverifystatus") \
            -> typing.Dict[str, typing.Any]:
        """

        @param guid:
        @param module:
        @param action:
        @return:
        """
        data: typing.Dict[str, str] = {
            "guid": guid,
            "module": module,
            "action": action
        }
        async with self.session.get(url="https://api.etherscan.io/api", data=data) as response:
            return await response.json()

    async def check_contract_execution_status(self, txhash: str) -> typing.Dict[str, typing.Any]:
        """
        (if there was an error during contract execution)
        Note: isError":"0" = Pass , isError":"1" = Error during Contract Execution
        @param txhash:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=transaction&action=getstatus&txhash={txhash}&apikey={self.api}") as response:
            return await response.json()

    async def block_and_uncle_rewards_by_blockno(self, blockno: typing.Union[int, str]) -> typing.Dict[str, typing.Any]:
        """
        Get Block And Uncle Rewards by BlockNo
        @param blockno:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=block&action=getblockreward&blockno={blockno}&apikey={self.api}") as response:
            return await response.json()

    async def check_transaction_receipt_status(self, txhash: str) -> typing.Dict[str, typing.Any]:
        """
        (Only applicable for Post Byzantium fork transactions)
        Note: status: 0 = Fail, 1 = Pass. Will return null/empty value for pre-byzantium fork
        @param txhash:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=transaction&action=gettxreceiptstatus&txhash={txhash}&apikey={self.api}") as response:
            return await response.json()

    async def estimated_block_countdown_time_by_blockno(self, blockno: typing.Union[int, str]) -> typing.Dict[
        str, typing.Any]:
        """
        Get Estimated Block Countdown Time by BlockNo
        @param blockno:
        @return:
        """
        async with self.session.get(
                f"https://api.etherscan.io/api?module=block&action=getblockcountdown&blockno={blockno}&apikey={self.api}") as response:
            return await response.json()

    async def list_of_ERC20_token_transfer_events__by_address(self, address: str, start_block: int = 0,
                                                              end_block: int = 999999999,
                                                              offset: typing.Optional[typing.Union[str, int]] = None,
                                                              page: typing.Optional[typing.Union[int, str]] = None) -> \
            typing.Dict[
                str, typing.Any]:
        """
        [Optional Parameters] startblock: starting blockNo to retrieve results, endblock: ending blockNo to retrieve results
        http://api.etherscan.io/api?module=account&action=tokentx&address=0x4e83362442b8d1bec281594cea3050c8eb01311c&startblock=0&endblock=999999999&sort=asc&apikey=YourApiKeyToken
        (Returns up to a maximum of the last 10000 transactions only)
        or
        https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2&page=1&offset=100&sort=asc&apikey=YourApiKeyToken
        (To get paginated results use page=<page number> and offset=<max records to return>)
        or
        https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2&address=0x4e83362442b8d1bec281594cea3050c8eb01311c&page=1&offset=100&sort=asc&apikey=YourApiKeyToken
        (To get transfer events for a specific token contract, include the contractaddress paramter)
        @param address:
        @param start_block:
        @param end_block:
        @param offset:
        @param page:
        @return:
        """
        link = f"http://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock={start_block}&endblock={end_block}&sort=asc&apikey={self.api} "
        if not (offset is None):
            link += f"&offset={offset}"
        if not (page is None):
            link += f"&page={page}"
        async with self.session.get(link) as response:
            return await response.json()

    async def list_of_blocks_mined_by_address(self, address: str,
                                              offset: typing.Optional[typing.Union[str, int]] = None,
                                              page: typing.Optional[typing.Union[int, str]] = None) -> \
            typing.Dict[
                str, typing.Any]:
        """
        https://api.etherscan.io/api?module=account&action=getminedblocks&address=0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b&blocktype=blocks&apikey=YourApiKeyToken
        or
        https://api.etherscan.io/api?module=account&action=getminedblocks&address=0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b&blocktype=blocks&page=1&offset=10&apikey=YourApiKeyToken
        (To get paginated results use page=<page number> and offset=<max records to return>)
        ** type = blocks (full blocks only) or uncles (uncle blocks only)
        @param address:
        @param offset:
        @param page:
        @return:
        """
        link: str = f"https://api.etherscan.io/api?module=account&action=getminedblocks&address={address}&blocktype=blocks&apikey={self.api}"
        if not (offset is None):
            link += f"&offset={offset}"
        if not (page is None):
            link += f"page={page}"
        async with self.session.get(link) as response:
            return await response.json()


import asyncio


async def main():
    f = Etherscan(api_key="")
    await f.open_session()
    print(await f.list_of_blocks_mined_by_address("0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b",page=1,offset=1))
    await f.close()


asyncio.run(main())
