#include <iostream>
#include <string>
#include <vector>
#include <memory>

class KitchenObserver {
public:
    virtual ~KitchenObserver() = default;
    virtual void onOrderEvent(const std::string& eventType, const std::string& orderId, const std::string& item, const std::string& station) = 0;
};

class ColdStationDisplay : public KitchenObserver {
public:
    void onOrderEvent(const std::string& eventType, const std::string& orderId, const std::string& item, const std::string& station) override {
        if (station == "COLD" || station == "ALL") {
            std::cout << "[Cold Station] Received " << eventType << " for Order #" << orderId << ": " << item << std::endl;
        }
    }
};

class HotStationDisplay : public KitchenObserver {
public:
    void onOrderEvent(const std::string& eventType, const std::string& orderId, const std::string& item, const std::string& station) override {
        if (station == "HOT" || station == "ALL") {
            std::cout << "[Hot Station] Received " << eventType << " for Order #" << orderId << ": " << item << std::endl;
        }
    }
};

class WaiterTerminal : public KitchenObserver {
public:
    void onOrderEvent(const std::string& eventType, const std::string& orderId, const std::string& item, const std::string& station) override {
        if (eventType == "ITEM_READY") {
            std::cout << "[Waiter Terminal] Ready to serve Order #" << orderId << " (" << item << " from " << station << ")" << std::endl;
        }
    }
};

class KitchenSubject {
    std::vector<std::shared_ptr<KitchenObserver>> observers;
public:
    void subscribe(std::shared_ptr<KitchenObserver> obs) { observers.push_back(obs); }
    void notifyAll(const std::string& eventType, const std::string& orderId, const std::string& item, const std::string& station) {
        for (auto& obs : observers) {
            obs->onOrderEvent(eventType, orderId, item, station);
        }
    }
};

int main() {
    KitchenSubject kitchen;
    kitchen.subscribe(std::make_shared<ColdStationDisplay>());
    kitchen.subscribe(std::make_shared<HotStationDisplay>());
    kitchen.subscribe(std::make_shared<WaiterTerminal>());

    std::cout << "Test 1 - Dispatch New Salad (COLD):" << std::endl;
    kitchen.notifyAll("NEW_ORDER", "101", "Classic Caesar Salad", "COLD");

    std::cout << "Test 2 - Dispatch New Steak (HOT):" << std::endl;
    kitchen.notifyAll("NEW_ORDER", "102", "Prime Ribeye Steak", "HOT");

    std::cout << "Test 3 - Mark Steak Ready:" << std::endl;
    kitchen.notifyAll("ITEM_READY", "102", "Prime Ribeye Steak", "HOT");

    return 0;
}
