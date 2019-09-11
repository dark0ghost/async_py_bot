# This Python file uses the following encoding: utf-8

import aiohttp

from typing import Dict


class CryptoPrice:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        """

        :param session:
        """
        self.api_link: str = "https://api.coingecko.com/api/v3/"
        self.obj: Dict[str, str] = dict()
        self.session: aiohttp.ClientSession = session

    def __len__(self) -> int:
        """
        Get len coin
        :return:
        """
        return len(self.obj)

    async def coin_list(self) -> Dict[str,str]:
        """
        List all supported coins id, name and symbol (no pagination required)
        Use this to obtain all the coins’ id in order to make API calls
        :return:
        """
        async with self.session.get(url=self.api_link + 'coins/list') as response:
            data = await response.json(content_type="application/json", encoding="utf-8")
            for i in data:
                self.obj[i["symbol"]] = {
                    'name': i["name"],
                    'id': i["id"]
                }
        return self.obj

    async def ping(self) -> Dict[str, str]:
        """
        Get status response from  api
        :return:
        """
        async with self.session.get(self.api_link + "ping") as response:
            return await response.json()

    async def exchanges(self) -> Dict[str, str]:
        """

        :return:
        """
        async with self.session.get(self.api_link + "exchanges") as response:
            return await response.json()

    async def exchanges_list(self) -> Dict[str, str]:
        async with self.session.get(self.api_link + "exchanges/list") as response:
            return await response.json()

    async def fetch_global(self) -> Dict[str, str]:
        """
        Get cryptocurrency global data

        :return:
        """
        async with self.session.get(self.api_link + "global") as response:
            return await response.json()

    async def exchange_rates(self) -> Dict:
        """
        Get BTC-to-Currency exchange rates

        :return:
        """
        async with self.session.get(self.api_link + "exchange_rates") as response:
            return (await response.json())['rates']

    async def events_types(self) -> Dict[str, str]:
        """


        :return:
        """
        async with self.session.get(self.api_link + "events/types") as response:
            return await response.json()

    async def events_countries(self) -> Dict[str, str]:
        """

        :return:
        """

        async with self.session.get(self.api_link + "events/countries") as response:
            return await response.json()

    async def events(self, country_code: str = '', Type: str = '', page: int = 100, upcoming_events_only: str = '',
                     rom_date: str = '', to_date: str = "") -> Dict[str, str]:
        """

        :param to_date:
        :param upcoming_events_only:
        :param Type:
        :param page:
        :param country_code:
        :type rom_date: object
        """
        async with self.session.get(
                self.api_link + f"events/countries?country_code={country_code}&type={Type}&page={page}&upcoming_events_only={upcoming_events_only}&romdate={rom_date}&to_date={to_date}") as response:
            return await response.json()

    async def status_updates_coin(self, id_coin: str = "bitcoin", per_page: int = 1, page: int = 1) -> Dict[str, str]:
        """
        :param page: int
        :param per_page: int
        :type id_coin: str
        """
        async with self.session.get(
                self.api_link + f"coins/{id_coin}/status_updates?per_page={per_page}&page={page}") as response:
            return await response.json()

    async def info_from_addres(self, id: int, contract_address: str) -> Dict[str, str]:
        """
        Asset platform (only ethereum is supported at this moment)
        Get coin info from contract address
        
        :type contract_address: object
        :return:
        """
        async with self.session.get(self.api_link + f"coins/{id}/contract/{contract_address}") as response:
            return await response.json()

    async def market_chart(self, id_: str, contract_address: str, vs_currency: str = "", days: str = "") -> Dict[str, str]:
        """
        Get historical market data include price, market cap, and 24h volume (granularity auto)
        Minutely data will be used for duration within 1 day, Hourly data will be used for duration between 1 day and 90 days, Daily data will be used for duration above 90 days.
        :param vs_currency:
        :param id_:
        :param contract_address:
        :type days: object
        """
        async with self.session.get(
                self.api_link + f"coins/{id_}/contract/{contract_address}/market_chart?vs_currency={vs_currency}&days={days}") as response:
            return await response.json()

    async def market_chart_range(self, id_: str, contract_address: str, vs_currency: str = "", from_: str = "",
                                 to: str = "") -> Dict[str, str]:
        """
        Get historical market data include price, market cap, and 24h volume within a range of timestamp (granularity auto)
        Minutely data will be used for duration within 1 day, Hourly data will be used for duration between 1 day and 90 days, Daily data will be used for duration above 90 days.
        :param to:
        :param vs_currency:
        :param id_:
        :param contract_address:
        :type from_: object
        """
        async with self.session.get(
                self.api_link + f"coins/{id_}/contract/{contract_address}/market_chart?vs_currency={vs_currency}&from={from_}&to={to}") as response:
            return await response.json()

    async def history_coin(self, coin: str, date: str, local: str = "") -> Dict[str, str]:
        """
        Get historical data (name, price, market, stats) at a given date for a coin
        :param coin:
        :param date:
        :param local:
        :return:
        """
        async with self.session.get(
                self.api_link + f"coins/{coin}/history?date={date}&localization={local}") as response:
            return await response.json()

    async def tickers(self, coin: str, exchange_ids: str = '', include_exchange_logo: str = '', page: int = 1,
                      order: str = "") -> Dict[str, str]:
        """
        Get coin tickers (paginated to 100 items)

        IMPORTANT:
        Ticker is_stale is true when ticker that has not been updated/unchanged from the exchange for a while.
        Ticker is_anomaly is true if ticker’s price is outliered by our system.
        You are responsible for managing how you want to display these information (e.g. footnote, different background, change opacity, hide)

        :param coin:
        :param exchange_ids:
        :param include_exchange_logo:
        :param page:
        :param order:
        :return:
        """
        async with self.session.get(
                self.api_link + f"coins/{coin}/tickers?exchange_ids={exchange_ids}&include_exchange_logo={include_exchange_logo}&page=10&order={order}&page={page}") as response:
            return await response.json()

    async def current_data(self, coin: str, localization: str = '', tickers: bool = False, market_data: bool = False,
                           community_data: bool = False, developer_data: bool = False, sparkline: bool = False) -> Dict[str, str]:
        """
        Get current data (name, price, market, ... including exchange tickers) for a coin
        :param sparkline:
        :param market_data:
        :param tickers:
        :param coin:
        :param localization:
        :param developer_data:
        :type community_data: object
        :return:
        """
        async with self.session.get(
                self.api_link + f"coins/{coin}?localization={localization}&tickers={tickers}&market_data={market_data}&community_data={community_data}&developer_data={developer_data}&sparkline={sparkline}") as response:
            return await response.json()

    async def coins_markets(self, vs_currency: str = "usd", order: str = "market_cap_desc", per_page: int = 100,
                            page: int = 1, sparkline: bool = "false", price_change_percentage: str = "24h") -> Dict[str, str]:
        """
        Use this to obtain all the coins market data (price, market cap, volume)
        :param vs_currency:
        :param order:
        :param per_page:
        :param page:
        :param sparkline:
        :param price_change_percentage:
        :return:
        """
        async with self.session.get(
                self.api_link + f"coins/markets?vs_currency={vs_currency}&order={order}&per_page={per_page}&page={page}&sparkline={sparkline}&price_change_percentage={price_change_percentage}") as response:
            return await response.json()

    async def simple_token_price(self, contract_addresses: str, coin: str = "ethereum",
                                 vs_currency: str = "usd") -> Dict[str, str]:
        """
        Get current price of tokens (using contract addresses) for a given platform in any other currency that you need.
        :param contract_addresses:
        :param coin:
        :param vs_currency:
        :return:
        """
        async with self.session.get(
                self.api_link + f"simple/token_price/{coin}?contract_addresses={contract_addresses}&vs_currencies={vs_currency}"
        ) as response:
            return await response.json()

    async def simple_price(self, ids: str, vs_currestring: str = "usd", include_market_cap: str = "false",
                           include_24hr_vol: str = "false", include_24hr_change: str = "false",
                           include_last_updated_at: str = "false") -> Dict[str, str]:
        """
        Get the current price of any cryptocurrencies in any other supported currencies that you need.
        :param include_last_updated_at:
        :param include_24hr_change:
        :param include_24hr_vol:
        :param include_market_cap:
        :param ids:
        :param vs_currestring:
        :return:
        """

        async with self.session.get(
                self.api_link + f"simple/price?ids={ids}&vs_currencies={vs_currestring}&include_market_cap={include_market_cap},include_24hr_vol={include_24hr_vol}&include_24hr_change={include_24hr_change}&include_last_updated_at={include_last_updated_at}"
        ) as response:
            return await response.json()

    async def supported_vs_currencies(self) -> Dict[str, str]:
        async with self.session.get(
                self.api_link + "simple/supported_vs_currencies"
        ) as response:
            return await response.json()
