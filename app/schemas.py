from decimal import Decimal
from uuid import UUID

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
    client_order_id: str | None = Field(..., example="my_order_id_1")
    symbol: str = Field(..., example="BTCUSDT")
    side: OrderSide = Field(..., example=OrderSide.BUY)
    type: OrderType = Field(..., example=OrderType.MARKET)
    time_in_force: TimeInForce = Field(..., example="GTC")
    quantity: Decimal = Field(..., example=Decimal("0.001"))
    price: Decimal | None = Field(..., example=Decimal("400.12"))
    stop_price: Decimal | None = Field(..., example=Decimal("400.12"))
    trailing_delta: Decimal | None = Field(..., example=Decimal("0.01"))


class OrderSchema(BaseModel):
    order_id: str | int | UUID = Field(..., example="1")
    client_order_id: str | None = Field(..., example="my_order_id_1")
    symbol: str = Field(..., example="BTCUSDT")
    status: str = Field(..., example="FILLED")
    executed_qty: Decimal = Field(
        default=Decimal("0.0"),
        example=Decimal("0.001"),
    )
    side: OrderSide = Field(..., example=OrderSide.BUY)
    type: OrderType = Field(..., example=OrderType.MARKET)
    time_in_force: TimeInForce = Field(..., example="GTC")
    price: Decimal | None = Field(..., example=Decimal("400.12"))
    stop_price: Decimal | None = Field(..., example=Decimal("400.12"))
