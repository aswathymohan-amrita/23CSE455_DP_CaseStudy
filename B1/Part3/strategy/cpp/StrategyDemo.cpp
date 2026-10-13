#include <iostream>
#include <string>
#include <memory>
#include <iomanip>

class PaymentStrategy {
public:
    virtual ~PaymentStrategy() = default;
    virtual std::string processPayment(double amount) = 0;
};

class CashPayment : public PaymentStrategy {
    double tendered;
public:
    CashPayment(double tendered) : tendered(tendered) {}
    std::string processPayment(double amount) override {
        if (tendered < amount) return "FAILED: Tendered $" + std::to_string(tendered) + " < Total $" + std::to_string(amount);
        double change = tendered - amount;
        return "SUCCESS [CASH]: Paid $" + std::to_string(amount).substr(0, 5) + " | Change due: $" + std::to_string(change).substr(0, 4);
    }
};

class StripeCardPayment : public PaymentStrategy {
    std::string cardNumber;
public:
    StripeCardPayment(std::string cardNumber) : cardNumber(cardNumber) {}
    std::string processPayment(double amount) override {
        std::string last4 = cardNumber.substr(cardNumber.length() - 4);
        return "SUCCESS [STRIPE]: Charged $" + std::to_string(amount).substr(0, 5) + " to card ending in " + last4 + " (tx_stripe_9821)";
    }
};

class MobilePayPayment : public PaymentStrategy {
    std::string provider;
public:
    MobilePayPayment(std::string provider) : provider(provider) {}
    std::string processPayment(double amount) override {
        return "SUCCESS [MOBILE]: Authorized $" + std::to_string(amount).substr(0, 5) + " via " + provider + " (ref_qr_5541)";
    }
};

class CheckoutContext {
    std::shared_ptr<PaymentStrategy> strategy;
public:
    void setStrategy(std::shared_ptr<PaymentStrategy> s) { strategy = s; }
    std::string checkout(double amount) {
        if (!strategy) return "FAILED: No payment strategy set";
        return strategy->processPayment(amount);
    }
};

int main() {
    CheckoutContext checkout;
    double orderTotal = 42.50;

    checkout.setStrategy(std::make_shared<StripeCardPayment>("4242-4242-4242-1234"));
    std::cout << "Test 1 - Stripe: " << checkout.checkout(orderTotal) << std::endl;

    checkout.setStrategy(std::make_shared<CashPayment>(50.00));
    std::cout << "Test 2 - Cash:   " << checkout.checkout(orderTotal) << std::endl;

    checkout.setStrategy(std::make_shared<MobilePayPayment>("ApplePay"));
    std::cout << "Test 3 - Mobile: " << checkout.checkout(orderTotal) << std::endl;

    return 0;
}
