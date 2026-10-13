#include <iostream>
#include <string>
#include <memory>

class TableContext;

class TableState {
public:
    virtual ~TableState() = default;
    virtual void occupy(TableContext* ctx) = 0;
    virtual void placeOrder(TableContext* ctx) = 0;
    virtual void requestBill(TableContext* ctx) = 0;
    virtual void settleAndClean(TableContext* ctx) = 0;
    virtual std::string getStatusName() const = 0;
};

class TableContext {
    std::shared_ptr<TableState> state;
    int tableNumber;
public:
    TableContext(int num);
    void setState(std::shared_ptr<TableState> s) { state = s; }
    std::string getStatus() const { return state->getStatusName(); }
    void occupy();
    void placeOrder();
    void requestBill();
    void settleAndClean();
};

class AvailableState : public TableState {
public:
    void occupy(TableContext* ctx) override;
    void placeOrder(TableContext* ctx) override { std::cout << "  Error: Cannot place order on empty table!" << std::endl; }
    void requestBill(TableContext* ctx) override { std::cout << "  Error: No bill on empty table!" << std::endl; }
    void settleAndClean(TableContext* ctx) override { std::cout << "  Note: Table is already available." << std::endl; }
    std::string getStatusName() const override { return "AVAILABLE"; }
};

class OccupiedState : public TableState {
public:
    void occupy(TableContext* ctx) override { std::cout << "  Error: Table is already occupied!" << std::endl; }
    void placeOrder(TableContext* ctx) override;
    void requestBill(TableContext* ctx) override { std::cout << "  Error: Order must be placed before requesting bill!" << std::endl; }
    void settleAndClean(TableContext* ctx) override;
    std::string getStatusName() const override { return "OCCUPIED"; }
};

class OrderPlacedState : public TableState {
public:
    void occupy(TableContext* ctx) override { std::cout << "  Error: Table is already occupied with an active order!" << std::endl; }
    void placeOrder(TableContext* ctx) override { std::cout << "  Action: Added more items to existing order." << std::endl; }
    void requestBill(TableContext* ctx) override;
    void settleAndClean(TableContext* ctx) override { std::cout << "  Error: Must pay bill before cleaning!" << std::endl; }
    std::string getStatusName() const override { return "ORDER_PLACED"; }
};

class BilledState : public TableState {
public:
    void occupy(TableContext* ctx) override { std::cout << "  Error: Table is currently in payment phase!" << std::endl; }
    void placeOrder(TableContext* ctx) override { std::cout << "  Error: Bill already printed; re-open order first." << std::endl; }
    void requestBill(TableContext* ctx) override { std::cout << "  Action: Re-printed bill receipt." << std::endl; }
    void settleAndClean(TableContext* ctx) override;
    std::string getStatusName() const override { return "BILLED"; }
};

// Implementations connecting states
void AvailableState::occupy(TableContext* ctx) {
    std::cout << "  Action: Seating party -> Transition to OCCUPIED" << std::endl;
    ctx->setState(std::make_shared<OccupiedState>());
}
void OccupiedState::placeOrder(TableContext* ctx) {
    std::cout << "  Action: Waiter sent order to kitchen -> Transition to ORDER_PLACED" << std::endl;
    ctx->setState(std::make_shared<OrderPlacedState>());
}
void OccupiedState::settleAndClean(TableContext* ctx) {
    std::cout << "  Action: Guests left before ordering -> Transition to AVAILABLE" << std::endl;
    ctx->setState(std::make_shared<AvailableState>());
}
void OrderPlacedState::requestBill(TableContext* ctx) {
    std::cout << "  Action: Printed guest bill -> Transition to BILLED" << std::endl;
    ctx->setState(std::make_shared<BilledState>());
}
void BilledState::settleAndClean(TableContext* ctx) {
    std::cout << "  Action: Payment received, table sanitized -> Transition to AVAILABLE" << std::endl;
    ctx->setState(std::make_shared<AvailableState>());
}

TableContext::TableContext(int num) : tableNumber(num), state(std::make_shared<AvailableState>()) {}
void TableContext::occupy() { state->occupy(this); }
void TableContext::placeOrder() { state->placeOrder(this); }
void TableContext::requestBill() { state->requestBill(this); }
void TableContext::settleAndClean() { state->settleAndClean(this); }

int main() {
    TableContext table(5);
    std::cout << "Initial State: Table #5 is " << table.getStatus() << std::endl;

    std::cout << "Test 1: Seating guests" << std::endl;
    table.occupy();
    std::cout << "State: " << table.getStatus() << std::endl;

    std::cout << "Test 2: Placing order" << std::endl;
    table.placeOrder();
    std::cout << "State: " << table.getStatus() << std::endl;

    std::cout << "Test 3: Requesting bill" << std::endl;
    table.requestBill();
    std::cout << "State: " << table.getStatus() << std::endl;

    std::cout << "Test 4: Settling bill and cleaning" << std::endl;
    table.settleAndClean();
    std::cout << "Final State: Table #5 is " << table.getStatus() << std::endl;

    return 0;
}
