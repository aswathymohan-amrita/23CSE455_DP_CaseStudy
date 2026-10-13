from abc import ABC, abstractmethod

class OrderProcessingPipeline(ABC):
    def process_order(self, order_id: str, subtotal: float):
        print(f"Processing Order #{order_id} (Subtotal: ${subtotal:.2f})")
        self._validate_order()
        total = self._calculate_total(subtotal)
        self._send_kitchen_ticket(order_id)
        self._notify_customer(order_id, total)
        print(f"Order #{order_id} fulfilled successfully.\n")

    def _validate_order(self):
        print("  Step 1 [Common]: Verified inventory and active kitchen capacity.")

    def _send_kitchen_ticket(self, order_id: str):
        print("  Step 3 [Common]: Dispatched ticket to kitchen display.")

    @abstractmethod
    def _calculate_total(self, subtotal: float) -> float: pass

    @abstractmethod
    def _notify_customer(self, order_id: str, final_total: float): pass

class DineInPipeline(OrderProcessingPipeline):
    def __init__(self, table_number: int):
        self.table_number = table_number

    def _calculate_total(self, subtotal: float) -> float:
        tax = subtotal * 0.0825
        total = subtotal + tax
        print(f"  Step 2 [Dine-In]: Added 8.25% dine-in tax (${tax:.2f}) -> Final: ${total:.2f}")
        return total

    def _notify_customer(self, order_id: str, final_total: float):
        print(f"  Step 4 [Dine-In]: Displayed order on Table #{self.table_number} waiter console.")

class OnlineDeliveryPipeline(OrderProcessingPipeline):
    def __init__(self, delivery_address: str):
        self.delivery_address = delivery_address

    def _calculate_total(self, subtotal: float) -> float:
        tax = subtotal * 0.0825
        delivery_fee = 4.99
        total = subtotal + tax + delivery_fee
        print(f"  Step 2 [Delivery]: Added tax (${tax:.2f}) + $4.99 delivery fee -> Final: ${total:.2f}")
        return total

    def _notify_customer(self, order_id: str, final_total: float):
        print(f"  Step 4 [Delivery]: Sent SMS tracking link to courier en route to {self.delivery_address}")

if __name__ == "__main__":
    dine_in = DineInPipeline(8)
    print("--- Test 1: Dine-In Pipeline ---")
    dine_in.process_order("DINE-301", 50.00)

    delivery = OnlineDeliveryPipeline("450 Elm Street")
    print("--- Test 2: Online Delivery Pipeline ---")
    delivery.process_order("DELV-902", 50.00)
