from abc import ABC, abstractmethod
from typing import List

class CartReceiver:
    def __init__(self):
        self.items: List[str] = []
        self.discount_percent: float = 0.0

    def add_item(self, item: str):
        self.items.append(item)

    def remove_item(self, item: str):
        if item in self.items:
            self.items.remove(item)

    def set_discount(self, pct: float):
        self.discount_percent = pct

    def print_cart(self):
        print(f"  Cart Items: {self.items} | Discount: {self.discount_percent * 100:.0f}%")

class POSCommand(ABC):
    @abstractmethod
    def execute(self): pass
    @abstractmethod
    def undo(self): pass

class AddItemCommand(POSCommand):
    def __init__(self, cart: CartReceiver, item: str):
        self.cart = cart
        self.item = item

    def execute(self):
        print(f"Execute: Add {self.item}")
        self.cart.add_item(self.item)

    def undo(self):
        print(f"Undo: Remove {self.item}")
        self.cart.remove_item(self.item)

class ApplyDiscountCommand(POSCommand):
    def __init__(self, cart: CartReceiver, new_discount: float):
        self.cart = cart
        self.new_discount = new_discount
        self.prev_discount = 0.0

    def execute(self):
        self.prev_discount = self.cart.discount_percent
        print(f"Execute: Apply {self.new_discount * 100:.0f}% Discount")
        self.cart.set_discount(self.new_discount)

    def undo(self):
        print(f"Undo: Revert discount back to {self.prev_discount * 100:.0f}%")
        self.cart.set_discount(self.prev_discount)

class POSTerminalInvoker:
    def __init__(self):
        self.history: List[POSCommand] = []

    def run_command(self, cmd: POSCommand):
        cmd.execute()
        self.history.append(cmd)

    def undo_last(self):
        if self.history:
            cmd = self.history.pop()
            cmd.undo()
        else:
            print("Nothing to undo!")

if __name__ == "__main__":
    cart = CartReceiver()
    pos = POSTerminalInvoker()

    print("Step 1: Adding Burger and Fries")
    pos.run_command(AddItemCommand(cart, "Classic Burger"))
    pos.run_command(AddItemCommand(cart, "Truffle Fries"))
    cart.print_cart()

    print("Step 2: Applying 15% VIP Discount")
    pos.run_command(ApplyDiscountCommand(cart, 0.15))
    cart.print_cart()

    print("Step 3: Cashier pressed Undo (reverting discount)")
    pos.undo_last()
    cart.print_cart()

    print("Step 4: Cashier pressed Undo (reverting Truffle Fries)")
    pos.undo_last()
    cart.print_cart()
