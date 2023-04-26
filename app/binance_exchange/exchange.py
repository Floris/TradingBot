from schemas import CreateOrderSchema


class BinanceExchange:
    def create_order(self, payload: CreateOrderSchema) -> dict:
        print("Creating order", payload.dict(exclude_none=True))
        return {}

    def get_order_by_id(self, order_id: str) -> dict:
        print("Getting order by id", order_id)
        return {}

    def get_all_orders(self) -> list[dict]:
        print("Getting all orders")
        return [{}]

    def cancel_order_by_id(self, order_id: str) -> None:
        print("Closing order by id", order_id)
        return

    def get_account(self) -> dict:
        print("Get account")
        return {}
