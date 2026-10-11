// Part 3 - Strategy demonstration (C++).
// Stripe and PayPal are simulated. This program does not call a network.

#include <iostream>
#include <string>

struct PaymentResult {
    std::string provider;
    std::string reference;
    double amount;
    std::string status;
};

class PaymentStrategy {
public:
    virtual ~PaymentStrategy() = default;
    virtual PaymentResult processPayment(double amount, const std::string& reference) = 0;
};

class StripePayment : public PaymentStrategy {
public:
    PaymentResult processPayment(double amount, const std::string& reference) override {
        return {"stripe", reference, amount, "paid"};
    }
};

class PayPalPayment : public PaymentStrategy {
public:
    PaymentResult processPayment(double amount, const std::string& reference) override {
        return {"paypal", reference, amount, "paid"};
    }
};

class BillingService {
public:
    explicit BillingService(PaymentStrategy& strategy) : strategy_(strategy) {}

    PaymentResult charge(double amount, const std::string& reference) {
        return strategy_.processPayment(amount, reference);
    }

private:
    PaymentStrategy& strategy_;
};

static void printResult(const PaymentResult& result) {
    std::cout << result.provider << " " << result.reference << " "
              << result.amount << " " << result.status << "\n";
}

int main() {
    StripePayment stripe;
    PayPalPayment paypal;
    BillingService stripeBill(stripe);
    BillingService paypalBill(paypal);
    const PaymentResult stripeResult = stripeBill.charge(1200.00, "DX-1001");
    const PaymentResult paypalResult = paypalBill.charge(850.50, "DX-1002");
    printResult(stripeResult);
    printResult(paypalResult);
    if (stripeResult.provider != "stripe" || paypalResult.provider != "paypal") {
        return 1;
    }
    return 0;
}
