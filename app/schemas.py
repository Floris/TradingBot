from decimal import Decimal

from enums import OrderSide, OrderType, TimeInForce
from pydantic import BaseModel, Field


class Signal(BaseModel):
    name: str
    reason: str
    action: OrderSide
    symbol: str
    price: Decimal
    stop_price: Decimal | None = None
    take_profit_price: Decimal | None = None


class CreateOrderSchema(BaseModel):
    symbol: str = Field(..., example="BTCUSDT")
    side: OrderSide = Field(..., example=OrderSide.BUY)
    type: OrderType = Field(..., example=OrderType.MARKET)
    time_in_force: TimeInForce = Field(..., example="GTC")
    quantity: Decimal | None = Field(..., example=Decimal("0.001"))
    price: Decimal | None = Field(..., example=Decimal("400.12"))
    client_order_id: str | None = Field(..., example="my_order_id_1")
    stop_price: Decimal | None = Field(..., example=Decimal("400.12"))
    trailing_delta: Decimal | None = Field(..., example=Decimal("0.01"))
