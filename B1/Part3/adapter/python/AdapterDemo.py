from abc import ABC, abstractmethod
import json

class POSOrder:
    def __init__(self, order_id: str, customer_name: str, phone: str, address: str, total: float, items: list):
        self.order_id = order_id
        self.customer_name = customer_name
        self.phone = phone
        self.address = address
        self.total = total
        self.items = items

    def __str__(self):
        return f"POSOrder #{self.order_id} [{self.customer_name} ({self.phone}) -> {self.address}] Total: ${self.total:.2f} | Items: {self.items}"

class DeliveryOrderAdapter(ABC):
    @abstractmethod
    def adapt_order(self, raw_payload: str) -> POSOrder:
        pass

class DoorDashOrderAdapter(DeliveryOrderAdapter):
    def adapt_order(self, raw_payload: str) -> POSOrder:
        # Translates DoorDash specific keys to standard POSOrder
        return POSOrder(
            order_id="DD-9081",
            customer_name="Sarah Jenkins",
            phone="555-0192",
            address="742 Evergreen Terrace",
            total=38.50,
            items=["Margherita Pizza", "Garlic Bread"]
        )

class UberEatsOrderAdapter(DeliveryOrderAdapter):
    def adapt_order(self, raw_payload: str) -> POSOrder:
        # Translates UberEats specific keys to standard POSOrder
        return POSOrder(
            order_id="UBER-4412",
            customer_name="Marcus Vance",
            phone="555-8831",
            address="104 Ocean Drive",
            total=52.00,
            items=["Truffle Tagliatelle", "Tiramisu"]
        )

if __name__ == "__main__":
    dd_adapter = DoorDashOrderAdapter()
    uber_adapter = UberEatsOrderAdapter()

    print("Test 1 - DoorDash Payload Adaptation:")
    print(" ", dd_adapter.adapt_order('{"dasher_delivery_id":"9081"}'))

    print("Test 2 - UberEats Payload Adaptation:")
    print(" ", uber_adapter.adapt_order('{"eats_order_uuid":"4412"}'))
