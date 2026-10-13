import java.util.*;

// Internal POS order representation
class POSOrder {
    public String orderId;
    public String customerName;
    public String customerPhone;
    public String deliveryAddress;
    public double totalPrice;
    public List<String> items = new ArrayList<>();

    public String toString() {
        return "POSOrder #" + orderId + " [" + customerName + " (" + customerPhone + ") -> " + deliveryAddress + "] Total: $" + String.format("%.2f", totalPrice) + " | Items: " + items;
    }
}

// Target interface expected by internal OrderService
interface DeliveryOrderAdapter {
    POSOrder adaptOrder(String rawPayload);
}

// Adaptee 1: DoorDash JSON simulation
class DoorDashOrderAdapter implements DeliveryOrderAdapter {
    public POSOrder adaptOrder(String rawPayload) {
        // Simulating parsing DoorDash specific keys: { "dasher_delivery_id", "consumer", "dropoff_address", "cart" }
        POSOrder order = new POSOrder();
        order.orderId = "DD-9081";
        order.customerName = "Sarah Jenkins";
        order.customerPhone = "555-0192";
        order.deliveryAddress = "742 Evergreen Terrace";
        order.totalPrice = 38.50;
        order.items.add("Margherita Pizza");
        order.items.add("Garlic Bread");
        return order;
    }
}

// Adaptee 2: UberEats JSON simulation
class UberEatsOrderAdapter implements DeliveryOrderAdapter {
    public POSOrder adaptOrder(String rawPayload) {
        // Simulating parsing UberEats specific keys: { "eats_order_uuid", "client_info", "destination", "order_lines" }
        POSOrder order = new POSOrder();
        order.orderId = "UBER-4412";
        order.customerName = "Marcus Vance";
        order.customerPhone = "555-8831";
        order.deliveryAddress = "104 Ocean Drive";
        order.totalPrice = 52.00;
        order.items.add("Truffle Tagliatelle");
        order.items.add("Tiramisu");
        return order;
    }
}

public class AdapterDemo {
    public static void main(String[] args) {
        DeliveryOrderAdapter ddAdapter = new DoorDashOrderAdapter();
        DeliveryOrderAdapter uberAdapter = new UberEatsOrderAdapter();

        System.out.println("Test 1 - DoorDash Payload Adaptation:");
        POSOrder ddOrder = ddAdapter.adaptOrder("{\"dasher_delivery_id\":\"9081\"}");
        System.out.println("  " + ddOrder);

        System.out.println("Test 2 - UberEats Payload Adaptation:");
        POSOrder uberOrder = uberAdapter.adaptOrder("{\"eats_order_uuid\":\"4412\"}");
        System.out.println("  " + uberOrder);
    }
}
