from abc import ABC, abstractmethod

class TableState(ABC):
    @abstractmethod
    def occupy(self, ctx): pass
    @abstractmethod
    def place_order(self, ctx): pass
    @abstractmethod
    def request_bill(self, ctx): pass
    @abstractmethod
    def settle_and_clean(self, ctx): pass
    @abstractmethod
    def get_status_name(self) -> str: pass

class AvailableState(TableState):
    def occupy(self, ctx):
        print("  Action: Seating party -> Transition to OCCUPIED")
        ctx.state = OccupiedState()
    def place_order(self, ctx):
        print("  Error: Cannot place order on empty table!")
    def request_bill(self, ctx):
        print("  Error: No bill on empty table!")
    def settle_and_clean(self, ctx):
        print("  Note: Table is already available.")
    def get_status_name(self) -> str: return "AVAILABLE"

class OccupiedState(TableState):
    def occupy(self, ctx):
        print("  Error: Table is already occupied!")
    def place_order(self, ctx):
        print("  Action: Waiter sent order to kitchen -> Transition to ORDER_PLACED")
        ctx.state = OrderPlacedState()
    def request_bill(self, ctx):
        print("  Error: Order must be placed before requesting bill!")
    def settle_and_clean(self, ctx):
        print("  Action: Guests left before ordering -> Transition to AVAILABLE")
        ctx.state = AvailableState()
    def get_status_name(self) -> str: return "OCCUPIED"

class OrderPlacedState(TableState):
    def occupy(self, ctx):
        print("  Error: Table is already occupied with an active order!")
    def place_order(self, ctx):
        print("  Action: Added more items to existing order.")
    def request_bill(self, ctx):
        print("  Action: Printed guest bill -> Transition to BILLED")
        ctx.state = BilledState()
    def settle_and_clean(self, ctx):
        print("  Error: Must pay bill before cleaning!")
    def get_status_name(self) -> str: return "ORDER_PLACED"

class BilledState(TableState):
    def occupy(self, ctx):
        print("  Error: Table is currently in payment phase!")
    def place_order(self, ctx):
        print("  Error: Bill already printed; re-open order first.")
    def request_bill(self, ctx):
        print("  Action: Re-printed bill receipt.")
    def settle_and_clean(self, ctx):
        print("  Action: Payment received, table sanitized -> Transition to AVAILABLE")
        ctx.state = AvailableState()
    def get_status_name(self) -> str: return "BILLED"

class TableContext:
    def __init__(self, table_number: int):
        self.table_number = table_number
        self.state = AvailableState()

    def get_status(self) -> str: return self.state.get_status_name()
    def occupy(self): self.state.occupy(self)
    def place_order(self): self.state.place_order(self)
    def request_bill(self): self.state.request_bill(self)
    def settle_and_clean(self): self.state.settle_and_clean(self)

if __name__ == "__main__":
    table = TableContext(5)
    print(f"Initial State: Table #5 is {table.get_status()}")

    print("Test 1: Seating guests")
    table.occupy()
    print("State:", table.get_status())

    print("Test 2: Placing order")
    table.place_order()
    print("State:", table.get_status())

    print("Test 3: Requesting bill")
    table.request_bill()
    print("State:", table.get_status())

    print("Test 4: Settling bill and cleaning")
    table.settle_and_clean()
    print(f"Final State: Table #5 is {table.get_status()}")
