import java.util.*;

// Receiver: Cart
class CartReceiver {
    private List<String> items = new ArrayList<>();
    private double discountPercent = 0.0;

    public void addItem(String item) { items.add(item); }
    public void removeItem(String item) { items.remove(item); }
    public void setDiscount(double pct) { discountPercent = pct; }
    public double getDiscount() { return discountPercent; }
    public void printCart() {
        System.out.println("  Cart Items: " + items + " | Discount: " + (discountPercent * 100) + "%");
    }
}

// Command Interface
interface POSCommand {
    void execute();
    void undo();
}

// Concrete Command: Add Item
class AddItemCommand implements POSCommand {
    private CartReceiver cart;
    private String item;
    public AddItemCommand(CartReceiver cart, String item) {
        this.cart = cart;
        this.item = item;
    }
    public void execute() {
        System.out.println("Execute: Add " + item);
        cart.addItem(item);
    }
    public void undo() {
        System.out.println("Undo: Remove " + item);
        cart.removeItem(item);
    }
}

// Concrete Command: Apply Discount
class ApplyDiscountCommand implements POSCommand {
    private CartReceiver cart;
    private double previousDiscount;
    private double newDiscount;
    public ApplyDiscountCommand(CartReceiver cart, double newDiscount) {
        this.cart = cart;
        this.newDiscount = newDiscount;
    }
    public void execute() {
        previousDiscount = cart.getDiscount();
        System.out.println("Execute: Apply " + (newDiscount * 100) + "% Discount");
        cart.setDiscount(newDiscount);
    }
    public void undo() {
        System.out.println("Undo: Revert discount back to " + (previousDiscount * 100) + "%");
        cart.setDiscount(previousDiscount);
    }
}

// Invoker: POS Terminal with Undo Stack
class POSTerminalInvoker {
    private Stack<POSCommand> history = new Stack<>();

    public void runCommand(POSCommand cmd) {
        cmd.execute();
        history.push(cmd);
    }

    public void undoLast() {
        if (!history.isEmpty()) {
            POSCommand cmd = history.pop();
            cmd.undo();
        } else {
            System.out.println("Nothing to undo!");
        }
    }
}

public class CommandDemo {
    public static void main(String[] args) {
        CartReceiver cart = new CartReceiver();
        POSTerminalInvoker pos = new POSTerminalInvoker();

        System.out.println("Step 1: Adding Burger and Fries");
        pos.runCommand(new AddItemCommand(cart, "Classic Burger"));
        pos.runCommand(new AddItemCommand(cart, "Truffle Fries"));
        cart.printCart();

        System.out.println("Step 2: Applying 15% VIP Discount");
        pos.runCommand(new ApplyDiscountCommand(cart, 0.15));
        cart.printCart();

        System.out.println("Step 3: Cashier pressed Undo (reverting discount)");
        pos.undoLast();
        cart.printCart();

        System.out.println("Step 4: Cashier pressed Undo (reverting Truffle Fries)");
        pos.undoLast();
        cart.printCart();
    }
}
