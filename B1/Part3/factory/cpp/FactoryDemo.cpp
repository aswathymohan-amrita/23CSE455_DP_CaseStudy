#include <iostream>
#include <string>
#include <vector>
#include <memory>

class KitchenTicket {
public:
    virtual ~KitchenTicket() = default;
    virtual std::string formatTicket(const std::string& orderId, const std::vector<std::string>& items) = 0;
};

class DineInTicket : public KitchenTicket {
    int tableNumber;
    std::string serverName;
public:
    DineInTicket(int tableNumber, const std::string& serverName) : tableNumber(tableNumber), serverName(serverName) {}
    std::string formatTicket(const std::string& orderId, const std::vector<std::string>& items) override {
        std::string res = "[DINE-IN TICKET #" + orderId + "] Table: " + std::to_string(tableNumber) + " | Server: " + serverName + " | Priority: NORMAL | Items: [";
        for (size_t i = 0; i < items.size(); ++i) {
            res += items[i] + (i + 1 < items.size() ? ", " : "");
        }
        return res + "]";
    }
};

class TakeoutTicket : public KitchenTicket {
    std::string pickupName;
public:
    TakeoutTicket(const std::string& pickupName) : pickupName(pickupName) {}
    std::string formatTicket(const std::string& orderId, const std::vector<std::string>& items) override {
        std::string res = "[TAKEOUT TICKET #" + orderId + "] Customer: " + pickupName + " | Packaging: BAG & UTENSILS | Items: [";
        for (size_t i = 0; i < items.size(); ++i) {
            res += items[i] + (i + 1 < items.size() ? ", " : "");
        }
        return res + "]";
    }
};

class DeliveryTicket : public KitchenTicket {
    std::string courier;
    std::string address;
public:
    DeliveryTicket(const std::string& courier, const std::string& address) : courier(courier), address(address) {}
    std::string formatTicket(const std::string& orderId, const std::vector<std::string>& items) override {
        std::string res = "[DELIVERY TICKET #" + orderId + "] Courier: " + courier + " | Address: " + address + " | SEAL REQUIRED | Items: [";
        for (size_t i = 0; i < items.size(); ++i) {
            res += items[i] + (i + 1 < items.size() ? ", " : "");
        }
        return res + "]";
    }
};

class TicketFactory {
public:
    static std::shared_ptr<KitchenTicket> createDineInTicket(int table, const std::string& server) {
        return std::make_shared<DineInTicket>(table, server);
    }
    static std::shared_ptr<KitchenTicket> createTakeoutTicket(const std::string& customer) {
        return std::make_shared<TakeoutTicket>(customer);
    }
    static std::shared_ptr<KitchenTicket> createDeliveryTicket(const std::string& courier, const std::string& address) {
        return std::make_shared<DeliveryTicket>(courier, address);
    }
};

int main() {
    std::vector<std::string> items = {"Burger", "Fries", "Coke"};

    auto t1 = TicketFactory::createDineInTicket(4, "Alex");
    std::cout << "Test 1: " << t1->formatTicket("101", items) << std::endl;

    auto t2 = TicketFactory::createTakeoutTicket("Emily R.");
    std::cout << "Test 2: " << t2->formatTicket("102", items) << std::endl;

    auto t3 = TicketFactory::createDeliveryTicket("DoorDash", "12 Maple St");
    std::cout << "Test 3: " << t3->formatTicket("103", items) << std::endl;

    return 0;
}
