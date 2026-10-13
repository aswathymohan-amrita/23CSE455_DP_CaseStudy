#include <iostream>
#include <string>
#include <vector>
#include <stack>
#include <memory>
#include <algorithm>

class CartReceiver {
    std::vector<std::string> items;
    double discountPercent = 0.0;
public:
    void addItem(const std::string& item) { items.push_back(item); }
    void removeItem(const std::string& item) {
        auto it = std::find(items.begin(), items.end(), item);
        if (it != items.end()) items.erase(it);
    }
    void setDiscount(double pct) { discountPercent = pct; }
    double getDiscount() const { return discountPercent; }
    void printCart() const {
        std::cout << "  Cart Items: [";
        for (size_t i = 0; i < items.size(); ++i) {
            std::cout << items[i] << (i + 1 < items.size() ? ", " : "");
        }
        std::cout << "] | Discount: " << static_cast<int>(discountPercent * 100) << "%" << std::endl;
    }
};

class POSCommand {
public:
    virtual ~POSCommand() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
};

class AddItemCommand : public POSCommand {
    CartReceiver* cart;
    std::string item;
public:
    AddItemCommand(CartReceiver* cart, const std::string& item) : cart(cart), item(item) {}
    void execute() override {
        std::cout << "Execute: Add " << item << std::endl;
        cart->addItem(item);
    }
    void undo() override {
        std::cout << "Undo: Remove " << item << std::endl;
        cart->removeItem(item);
    }
};

class ApplyDiscountCommand : public POSCommand {
    CartReceiver* cart;
    double newDiscount;
    double prevDiscount = 0.0;
public:
    ApplyDiscountCommand(CartReceiver* cart, double newDiscount) : cart(cart), newDiscount(newDiscount) {}
    void execute() override {
        prevDiscount = cart->getDiscount();
        std::cout << "Execute: Apply " << static_cast<int>(newDiscount * 100) << "% Discount" << std::endl;
        cart->setDiscount(newDiscount);
    }
    void undo() override {
        std::cout << "Undo: Revert discount back to " << static_cast<int>(prevDiscount * 100) << "%" << std::endl;
        cart->setDiscount(prevDiscount);
    }
};

class POSTerminalInvoker {
    std::stack<std::shared_ptr<POSCommand>> history;
public:
    void runCommand(std::shared_ptr<POSCommand> cmd) {
        cmd->execute();
        history.push(cmd);
    }
    void undoLast() {
        if (!history.empty()) {
            auto cmd = history.top();
            history.pop();
            cmd->undo();
        } else {
            std::cout << "Nothing to undo!" << std::endl;
        }
    }
};

int main() {
    CartReceiver cart;
    POSTerminalInvoker pos;

    std::cout << "Step 1: Adding Burger and Fries" << std::endl;
    pos.runCommand(std::make_shared<AddItemCommand>(&cart, "Classic Burger"));
    pos.runCommand(std::make_shared<AddItemCommand>(&cart, "Truffle Fries"));
    cart.printCart();

    std::cout << "Step 2: Applying 15% VIP Discount" << std::endl;
    pos.runCommand(std::make_shared<ApplyDiscountCommand>(&cart, 0.15));
    cart.printCart();

    std::cout << "Step 3: Cashier pressed Undo (reverting discount)" << std::endl;
    pos.undoLast();
    cart.printCart();

    std::cout << "Step 4: Cashier pressed Undo (reverting Truffle Fries)" << std::endl;
    pos.undoLast();
    cart.printCart();

    return 0;
}
