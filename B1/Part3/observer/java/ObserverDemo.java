import java.util.*;

interface KitchenObserver {
    void onOrderEvent(String eventType, String orderId, String item, String station);
}

class ColdStationDisplay implements KitchenObserver {
    public void onOrderEvent(String eventType, String orderId, String item, String station) {
        if ("COLD".equalsIgnoreCase(station) || "ALL".equalsIgnoreCase(station)) {
            System.out.println("[Cold Station] Received " + eventType + " for Order #" + orderId + ": " + item);
        }
    }
}

class HotStationDisplay implements KitchenObserver {
    public void onOrderEvent(String eventType, String orderId, String item, String station) {
        if ("HOT".equalsIgnoreCase(station) || "ALL".equalsIgnoreCase(station)) {
            System.out.println("[Hot Station] Received " + eventType + " for Order #" + orderId + ": " + item);
        }
    }
}

class WaiterTerminal implements KitchenObserver {
    public void onOrderEvent(String eventType, String orderId, String item, String station) {
        if ("ITEM_READY".equalsIgnoreCase(eventType)) {
            System.out.println("[Waiter Terminal] Ready to serve Order #" + orderId + " (" + item + " from " + station + ")");
        }
    }
}

class KitchenSubject {
    private List<KitchenObserver> observers = new ArrayList<>();
    public void subscribe(KitchenObserver obs) { observers.add(obs); }
    public void notifyAllObservers(String eventType, String orderId, String item, String station) {
        for (KitchenObserver obs : observers) {
            obs.onOrderEvent(eventType, orderId, item, station);
        }
    }
}

public class ObserverDemo {
    public static void main(String[] args) {
        KitchenSubject kitchen = new KitchenSubject();
        kitchen.subscribe(new ColdStationDisplay());
        kitchen.subscribe(new HotStationDisplay());
        kitchen.subscribe(new WaiterTerminal());

        System.out.println("Test 1 - Dispatch New Salad (COLD):");
        kitchen.notifyAllObservers("NEW_ORDER", "101", "Classic Caesar Salad", "COLD");

        System.out.println("Test 2 - Dispatch New Steak (HOT):");
        kitchen.notifyAllObservers("NEW_ORDER", "102", "Prime Ribeye Steak", "HOT");

        System.out.println("Test 3 - Mark Steak Ready:");
        kitchen.notifyAllObservers("ITEM_READY", "102", "Prime Ribeye Steak", "HOT");
    }
}
