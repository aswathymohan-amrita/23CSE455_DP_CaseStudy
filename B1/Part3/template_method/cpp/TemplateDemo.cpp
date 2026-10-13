#include <iostream>
#include <string>
#include <iomanip>

class OrderProcessingPipeline {
public:
    virtual ~OrderProcessingPipeline() = default;

    void processOrder(const std::string& orderId, double subtotal) {
        std::cout << "Processing Order #" << orderId << " (Subtotal: $" << subtotal << ")" << std::endl;
        validateOrder();
        double total = calculateTotal(subtotal);
        sendKitchenTicket(orderId);
        notifyCustomer(orderId, total);
        std::cout << "Order #" << orderId << " fulfilled successfully.\n" << std::endl;
    }

private:
    void validateOrder() {
        std::cout << "  Step 1 [Common]: Verified inventory and active kitchen capacity." << std::endl;
    }
    void sendKitchenTicket(const std::string& orderId) {
        std::cout << "  Step 3 [Common]: Dispatched ticket to kitchen display." << std::endl;
    }

protected:
    virtual double calculateTotal(double subtotal) = 0;
    virtual void notifyCustomer(const std::string& orderId, double finalTotal) = 0;
};

class DineInPipeline : public OrderProcessingPipeline {
    int tableNumber;
public:
    DineInPipeline(int tableNumber) : tableNumber(tableNumber) {}
    double calculateTotal(double subtotal) override {
        double tax = subtotal * 0.0825;
        double total = subtotal + tax;
        std::cout << "  Step 2 [Dine-In]: Added 8.25% dine-in tax ($" << tax << ") -> Final: $" << total << std::endl;
        return total;
    }
    void notifyCustomer(const std::string& orderId, double finalTotal) override {
        std::cout << "  Step 4 [Dine-In]: Displayed order on Table #" << tableNumber << " waiter console." << std::endl;
    }
};

class OnlineDeliveryPipeline : public OrderProcessingPipeline {
    std::string deliveryAddress;
public:
    OnlineDeliveryPipeline(const std::string& address) : deliveryAddress(address) {}
    double calculateTotal(double subtotal) override {
        double tax = subtotal * 0.0825;
        double deliveryFee = 4.99;
        double total = subtotal + tax + deliveryFee;
        std::cout << "  Step 2 [Delivery]: Added tax ($" << tax << ") + $4.99 delivery fee -> Final: $" << total << std::endl;
        return total;
    }
    void notifyCustomer(const std::string& orderId, double finalTotal) override {
        std::cout << "  Step 4 [Delivery]: Sent SMS tracking link to courier en route to " << deliveryAddress << std::endl;
    }
};

int main() {
    DineInPipeline dineIn(8);
    std::cout << "--- Test 1: Dine-In Pipeline ---" << std::endl;
    dineIn.processOrder("DINE-301", 50.00);

    OnlineDeliveryPipeline delivery("450 Elm Street");
    std::cout << "--- Test 2: Online Delivery Pipeline ---" << std::endl;
    delivery.processOrder("DELV-902", 50.00);

    return 0;
}
