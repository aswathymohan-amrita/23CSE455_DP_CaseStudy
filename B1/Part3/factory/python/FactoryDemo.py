from abc import ABC, abstractmethod
from typing import List

class KitchenTicket(ABC):
    @abstractmethod
    def format_ticket(self, order_id: str, items: List[str]) -> str:
        pass

class DineInTicket(KitchenTicket):
    def __init__(self, table_number: int, server_name: str):
        self.table_number = table_number
        self.server_name = server_name

    def format_ticket(self, order_id: str, items: List[str]) -> str:
        return f"[DINE-IN TICKET #{order_id}] Table: {self.table_number} | Server: {self.server_name} | Priority: NORMAL | Items: {items}"

class TakeoutTicket(KitchenTicket):
    def __init__(self, pickup_name: str):
        self.pickup_name = pickup_name

    def format_ticket(self, order_id: str, items: List[str]) -> str:
        return f"[TAKEOUT TICKET #{order_id}] Customer: {self.pickup_name} | Packaging: BAG & UTENSILS | Items: {items}"

class DeliveryTicket(KitchenTicket):
    def __init__(self, courier: str, address: str):
        self.courier = courier
        self.address = address

    def format_ticket(self, order_id: str, items: List[str]) -> str:
        return f"[DELIVERY TICKET #{order_id}] Courier: {self.courier} | Address: {self.address} | SEAL REQUIRED | Items: {items}"

class TicketFactory:
    @staticmethod
    def create_dine_in_ticket(table_number: int, server: str) -> KitchenTicket:
        return DineInTicket(table_number, server)

    @staticmethod
    def create_takeout_ticket(customer: str) -> KitchenTicket:
        return TakeoutTicket(customer)

    @staticmethod
    def create_delivery_ticket(courier: str, address: str) -> KitchenTicket:
        return DeliveryTicket(courier, address)

if __name__ == "__main__":
    items = ["Burger", "Fries", "Coke"]

    t1 = TicketFactory.create_dine_in_ticket(4, "Alex")
    print("Test 1:", t1.format_ticket("101", items))

    t2 = TicketFactory.create_takeout_ticket("Emily R.")
    print("Test 2:", t2.format_ticket("102", items))

    t3 = TicketFactory.create_delivery_ticket("DoorDash", "12 Maple St")
    print("Test 3:", t3.format_ticket("103", items))
