from decimal import Decimal
from uuid import uuid4

from config import MainConfig
from enums import OrderSide, OrderType, TimeInForce
from interfaces import CryptoExchangeProtocol
from schemas import CreateOrderSchema, OrderSchema


class TradeExecutor:
    def __init__(
        self, config: MainConfig, crypto_exchange: CryptoExchangeProtocol | None
    ):
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
