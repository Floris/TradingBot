from decimal import Decimal
from uuid import uuid4

from config.config import MainConfig
from enums import OrderSide, OrderType, TimeInForce
from interfaces import CryptoExchangeProtocol
from schemas import CreateOrderSchema, OrderSchema


class TradeExecutor:
    def __init__(
        self, config: MainConfig, crypto_exchange: CryptoExchangeProtocol | None
    ):
        """
        Initializes a new TradeExecutor instance.

        Args:
        - config: MainConfig instance, containing the main configuration.
        - crypto_exchange: CryptoExchangeProtocol instance, the crypto exchange to use.
        """
        self.config = config
        self.crypto_exchange = crypto_exchange

    def submit_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: Decimal,
        price: Decimal,
        stop_price: Decimal | None = None,
        trailing_delta: Decimal | None = None,
    ) -> OrderSchema:
        """
        Submits an order to the crypto exchange.

        Args:
        - symbol: str, the symbol to trade.
        - side: OrderSide instance, the order side.
        - quantity: Decimal, the order quantity.
        - price: Decimal, the order price.
        - stop_price: Decimal or None, the stop price for the order.
        - trailing_delta: Decimal or None, the trailing delta for the order.

        Returns:
        - An OrderSchema instance representing the executed order.
        """
        client_order_id = str(uuid4())
        payload = CreateOrderSchema(
            symbol=symbol,
            side=side,
            type=OrderType.MARKET,
            time_in_force=TimeInForce.GTC,
            quantity=quantity,
            price=price,
            client_order_id=client_order_id,
            stop_price=stop_price,
            trailing_delta=trailing_delta,
        )

        # Return fake order if backtesting or crypto_exchange is None
        if self.config.backtest or self.crypto_exchange is None:
            return OrderSchema(
                order_id=str(uuid4()),
                client_order_id=payload.client_order_id,
                symbol=payload.symbol,
                status="FILLED",
                executed_qty=payload.quantity,
                side=payload.side,
                type=payload.type,
                time_in_force=payload.time_in_force,
                price=payload.price,
                stop_price=payload.stop_price,
            )

        # Assumes order is filled immediately
        return self.crypto_exchange.create_order(payload)
