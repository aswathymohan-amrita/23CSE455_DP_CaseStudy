#include <iostream>
#include <string>
#include <vector>
#include <memory>

class POSOrder {
public:
    std::string orderId;
    std::string customerName;
    std::string phone;
    std::string address;
    double total;
    std::vector<std::string> items;

    void print() const {
        std::cout << "POSOrder #" << orderId << " [" << customerName << " (" << phone << ") -> " << address << "] Total: $" << total << " | Items: [";
        for (size_t i = 0; i < items.size(); ++i) {
            std::cout << items[i] << (i + 1 < items.size() ? ", " : "");
        }
        std::cout << "]" << std::endl;
    }
};

class DeliveryOrderAdapter {
public:
    virtual ~DeliveryOrderAdapter() = default;
    virtual POSOrder adaptOrder(const std::string& rawPayload) = 0;
};

class DoorDashOrderAdapter : public DeliveryOrderAdapter {
public:
    POSOrder adaptOrder(const std::string& rawPayload) override {
        POSOrder order;
        order.orderId = "DD-9081";
        order.customerName = "Sarah Jenkins";
        order.phone = "555-0192";
        order.address = "742 Evergreen Terrace";
        order.total = 38.50;
        order.items = {"Margherita Pizza", "Garlic Bread"};
        return order;
    }
};

class UberEatsOrderAdapter : public DeliveryOrderAdapter {
public:
    POSOrder adaptOrder(const std::string& rawPayload) override {
        POSOrder order;
        order.orderId = "UBER-4412";
        order.customerName = "Marcus Vance";
        order.phone = "555-8831";
        order.address = "104 Ocean Drive";
        order.total = 52.00;
        order.items = {"Truffle Tagliatelle", "Tiramisu"};
        return order;
    }
};

int main() {
    DoorDashOrderAdapter ddAdapter;
    UberEatsOrderAdapter uberAdapter;

    std::cout << "Test 1 - DoorDash Payload Adaptation:" << std::endl;
    std::cout << "  ";
    ddAdapter.adaptOrder("{\"dasher_delivery_id\":\"9081\"}").print();

    std::cout << "Test 2 - UberEats Payload Adaptation:" << std::endl;
    std::cout << "  ";
    uberAdapter.adaptOrder("{\"eats_order_uuid\":\"4412\"}").print();

    return 0;
}
