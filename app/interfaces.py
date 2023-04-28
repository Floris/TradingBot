from datetime import datetime
from typing import Protocol

import pandas
from config.config import MainConfig
from enums import INTERVALS
from schemas import CreateOrderSchema, OrderSchema, Signal


class MarketDataProtocol(Protocol):
    def get_klines(
        self,
        symbol: str,
        interval: INTERVALS,
        limit: int,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> pandas.DataFrame:
        """
        Get klines from the exchange.

        Args:
            symbol (str): The symbol to get klines for.
            interval (INTERVALS): The interval to get klines for.
            limit (int): The maximum number of klines to return.
            start_time (datetime | None): The start time for the klines. If None, will use the earliest available time.
            end_time (datetime | None): The end time for the klines. If None, will use the latest available time.

        Returns:
            pandas.DataFrame: A DataFrame containing klines data.
        """
        ...


class CryptoExchangeProtocol(Protocol):
    def create_order(self, payload: CreateOrderSchema) -> OrderSchema:
        """
        Creates a new order on the exchange.

        Args:
            payload (CreateOrderSchema): The order details.

        Returns:
            dict: A dictionary containing the order details.
        """
        ...

    def get_order_by_id(self, order_id: str) -> dict:
        """
        Retrieves an order by ID from the exchange.

        Args:
            order_id (str): The ID of the order to retrieve.

        Returns:
            dict: A dictionary containing the order details.
        """
        ...

    def get_all_orders(self) -> list[dict]:
        """
        Retrieves all orders from the exchange.

        Returns:
            list[dict]: A list of dictionaries containing the order details.
        """
        ...

    def cancel_order_by_id(self, order_id: str) -> None:
        """
        Cancels an order by ID on the exchange.

        Args:
            order_id (str): The ID of the order to cancel.
        """
        ...

    def get_account(self) -> dict:
        """
        Retrieves the account details from the exchange.

        Returns:
            dict: A dictionary containing the account details.
        """
        ...


class StrategyProtocol(Protocol):
    def initialize(
        self,
        config: MainConfig,
    ) -> None:
        """
        Initializes the strategy.

        Args:
            config (MainConfig): The configuration object.
        """
        ...

    def analyze(self, df: pandas.DataFrame) -> Signal | None:
        """
        Analyzes the klines DataFrame and generates a Signal if conditions are met.

        Args:
            df (pandas.DataFrame): A DataFrame containing klines data.

        Returns:
            Signal | None: A Signal object if conditions are met, otherwise None.
        """
        ...
