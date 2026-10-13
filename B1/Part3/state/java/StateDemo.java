// State pattern modeling Table Lifecycle: AVAILABLE -> OCCUPIED -> ORDER_PLACED -> BILLED -> AVAILABLE

interface TableState {
    void occupy(TableContext ctx);
    void placeOrder(TableContext ctx);
    void requestBill(TableContext ctx);
    void settleAndClean(TableContext ctx);
    String getStatusName();
}

class AvailableState implements TableState {
    public void occupy(TableContext ctx) {
        System.out.println("  Action: Seating party -> Transition to OCCUPIED");
        ctx.setState(new OccupiedState());
    }
    public void placeOrder(TableContext ctx) {
        System.out.println("  Error: Cannot place order on empty table!");
    }
    public void requestBill(TableContext ctx) {
        System.out.println("  Error: No bill on empty table!");
    }
    public void settleAndClean(TableContext ctx) {
        System.out.println("  Note: Table is already available.");
    }
    public String getStatusName() { return "AVAILABLE"; }
}

class OccupiedState implements TableState {
    public void occupy(TableContext ctx) {
        System.out.println("  Error: Table is already occupied!");
    }
    public void placeOrder(TableContext ctx) {
        System.out.println("  Action: Waiter sent order to kitchen -> Transition to ORDER_PLACED");
        ctx.setState(new OrderPlacedState());
    }
    public void requestBill(TableContext ctx) {
        System.out.println("  Error: Order must be placed before requesting bill!");
    }
    public void settleAndClean(TableContext ctx) {
        System.out.println("  Action: Guests left before ordering -> Transition to AVAILABLE");
        ctx.setState(new AvailableState());
    }
    public String getStatusName() { return "OCCUPIED"; }
}

class OrderPlacedState implements TableState {
    public void occupy(TableContext ctx) {
        System.out.println("  Error: Table is already occupied with an active order!");
    }
    public void placeOrder(TableContext ctx) {
        System.out.println("  Action: Added more items to existing order.");
    }
    public void requestBill(TableContext ctx) {
        System.out.println("  Action: Printed guest bill -> Transition to BILLED");
        ctx.setState(new BilledState());
    }
    public void settleAndClean(TableContext ctx) {
        System.out.println("  Error: Must pay bill before cleaning!");
    }
    public String getStatusName() { return "ORDER_PLACED"; }
}

class BilledState implements TableState {
    public void occupy(TableContext ctx) {
        System.out.println("  Error: Table is currently in payment phase!");
    }
    public void placeOrder(TableContext ctx) {
        System.out.println("  Error: Bill already printed; re-open order first.");
    }
    public void requestBill(TableContext ctx) {
        System.out.println("  Action: Re-printed bill receipt.");
    }
    public void settleAndClean(TableContext ctx) {
        System.out.println("  Action: Payment received, table sanitized -> Transition to AVAILABLE");
        ctx.setState(new AvailableState());
    }
    public String getStatusName() { return "BILLED"; }
}

class TableContext {
    private TableState state;
    private int tableNumber;

    public TableContext(int tableNumber) {
        this.tableNumber = tableNumber;
        this.state = new AvailableState();
    }
    public void setState(TableState state) { this.state = state; }
    public String getStatus() { return state.getStatusName(); }
    public void occupy() { state.occupy(this); }
    public void placeOrder() { state.placeOrder(this); }
    public void requestBill() { state.requestBill(this); }
    public void settleAndClean() { state.settleAndClean(this); }
}

public class StateDemo {
    public static void main(String[] args) {
        TableContext table = new TableContext(5);
        System.out.println("Initial State: Table #5 is " + table.getStatus());

        System.out.println("Test 1: Seating guests");
        table.occupy();
        System.out.println("State: " + table.getStatus());

        System.out.println("Test 2: Placing order");
        table.placeOrder();
        System.out.println("State: " + table.getStatus());

        System.out.println("Test 3: Requesting bill");
        table.requestBill();
        System.out.println("State: " + table.getStatus());

        System.out.println("Test 4: Settling bill and cleaning");
        table.settleAndClean();
        System.out.println("Final State: Table #5 is " + table.getStatus());
    }
}
