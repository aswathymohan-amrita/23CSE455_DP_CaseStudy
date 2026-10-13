// Template Method pattern defining the order fulfillment sequence

abstract class OrderProcessingPipeline {
    // Template Method: Defines the skeleton algorithm
    public final void processOrder(String orderId, double subtotal) {
        System.out.println("Processing Order #" + orderId + " (Subtotal: $" + String.format("%.2f", subtotal) + ")");
        validateOrder();
        double total = calculateTotal(subtotal);
        sendKitchenTicket(orderId);
        notifyCustomer(orderId, total);
        System.out.println("Order #" + orderId + " fulfilled successfully.\n");
    }

    private void validateOrder() {
        System.out.println("  Step 1 [Common]: Verified inventory and active kitchen capacity.");
    }

    private void sendKitchenTicket(String orderId) {
        System.out.println("  Step 3 [Common]: Dispatched ticket to kitchen display.");
    }

    // Primitive hooks overridden by subclasses
    protected abstract double calculateTotal(double subtotal);
    protected abstract void notifyCustomer(String orderId, double finalTotal);
}

// Concrete Pipeline 1: Dine-In Order
class DineInPipeline extends OrderProcessingPipeline {
    private int tableNumber;
    public DineInPipeline(int tableNumber) { this.tableNumber = tableNumber; }

    protected double calculateTotal(double subtotal) {
        double tax = subtotal * 0.0825; // 8.25% sales tax
        double total = subtotal + tax;
        System.out.println("  Step 2 [Dine-In]: Added 8.25% dine-in tax ($" + String.format("%.2f", tax) + ") -> Final: $" + String.format("%.2f", total));
        return total;
    }

    protected void notifyCustomer(String orderId, double finalTotal) {
        System.out.println("  Step 4 [Dine-In]: Displayed order on Table #" + tableNumber + " waiter console.");
    }
}

// Concrete Pipeline 2: Online Delivery Order
class OnlineDeliveryPipeline extends OrderProcessingPipeline {
    private String deliveryAddress;
    public OnlineDeliveryPipeline(String deliveryAddress) { this.deliveryAddress = deliveryAddress; }

    protected double calculateTotal(double subtotal) {
        double tax = subtotal * 0.0825;
        double deliveryFee = 4.99;
        double total = subtotal + tax + deliveryFee;
        System.out.println("  Step 2 [Delivery]: Added tax ($" + String.format("%.2f", tax) + ") + $4.99 delivery fee -> Final: $" + String.format("%.2f", total));
        return total;
    }

    protected void notifyCustomer(String orderId, double finalTotal) {
        System.out.println("  Step 4 [Delivery]: Sent SMS tracking link to courier en route to " + deliveryAddress);
    }
}

public class TemplateDemo {
    public static void main(String[] args) {
        OrderProcessingPipeline dineIn = new DineInPipeline(8);
        System.out.println("--- Test 1: Dine-In Pipeline ---");
        dineIn.processOrder("DINE-301", 50.00);

        OrderProcessingPipeline delivery = new OnlineDeliveryPipeline("450 Elm Street");
        System.out.println("--- Test 2: Online Delivery Pipeline ---");
        delivery.processOrder("DELV-902", 50.00);
    }
}
