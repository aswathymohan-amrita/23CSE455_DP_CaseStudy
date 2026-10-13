import java.util.*;

// Product Interface
interface KitchenTicket {
    String formatTicket(String orderId, List<String> items);
}

// Concrete Product 1: Dine-In
class DineInTicket implements KitchenTicket {
    private int tableNumber;
    private String serverName;
    public DineInTicket(int tableNumber, String serverName) {
        this.tableNumber = tableNumber;
        this.serverName = serverName;
    }
    public String formatTicket(String orderId, List<String> items) {
        return "[DINE-IN TICKET #" + orderId + "] Table: " + tableNumber + " | Server: " + serverName + " | Priority: NORMAL | Items: " + items;
    }
}

// Concrete Product 2: Takeout
class TakeoutTicket implements KitchenTicket {
    private String pickupName;
    public TakeoutTicket(String pickupName) { this.pickupName = pickupName; }
    public String formatTicket(String orderId, List<String> items) {
        return "[TAKEOUT TICKET #" + orderId + "] Customer: " + pickupName + " | Packaging: BAG & UTENSILS | Items: " + items;
    }
}

// Concrete Product 3: Delivery
class DeliveryTicket implements KitchenTicket {
    private String courier;
    private String address;
    public DeliveryTicket(String courier, String address) {
        this.courier = courier;
        this.address = address;
    }
    public String formatTicket(String orderId, List<String> items) {
        return "[DELIVERY TICKET #" + orderId + "] Courier: " + courier + " | Address: " + address + " | SEAL REQUIRED | Items: " + items;
    }
}

// Creator Factory
class TicketFactory {
    public static KitchenTicket createDineInTicket(int tableNumber, String server) {
        return new DineInTicket(tableNumber, server);
    }
    public static KitchenTicket createTakeoutTicket(String customer) {
        return new TakeoutTicket(customer);
    }
    public static KitchenTicket createDeliveryTicket(String courier, String address) {
        return new DeliveryTicket(courier, address);
    }
}

public class FactoryDemo {
    public static void main(String[] args) {
        List<String> items = Arrays.asList("Burger", "Fries", "Coke");

        KitchenTicket t1 = TicketFactory.createDineInTicket(4, "Alex");
        System.out.println("Test 1: " + t1.formatTicket("101", items));

        KitchenTicket t2 = TicketFactory.createTakeoutTicket("Emily R.");
        System.out.println("Test 2: " + t2.formatTicket("102", items));

        KitchenTicket t3 = TicketFactory.createDeliveryTicket("DoorDash", "12 Maple St");
        System.out.println("Test 3: " + t3.formatTicket("103", items));
    }
}
