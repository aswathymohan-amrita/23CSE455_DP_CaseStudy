/**
 * Part 3 - Strategy demonstration (Java).
 * BillingService depends on PaymentStrategy. Provider choice is made
 * by injecting a concrete strategy, not by an if/else inside the service.
 */

import java.util.Map;

interface PaymentStrategy {
    Map<String, String> processPayment(double amount, String reference);
}

class StripePayment implements PaymentStrategy {
    @Override
    public Map<String, String> processPayment(double amount, String reference) {
        return Map.of(
                "provider", "stripe",
                "reference", reference,
                "amount", String.valueOf(amount),
                "status", "paid");
    }
}

class PayPalPayment implements PaymentStrategy {
    @Override
    public Map<String, String> processPayment(double amount, String reference) {
        return Map.of(
                "provider", "paypal",
                "reference", reference,
                "amount", String.valueOf(amount),
                "status", "paid");
    }
}

class BillingService {
    private final PaymentStrategy strategy;

    BillingService(PaymentStrategy strategy) {
        this.strategy = strategy;
    }

    Map<String, String> charge(double amount, String reference) {
        return strategy.processPayment(amount, reference);
    }
}

public class StrategyDemo {
    public static void main(String[] args) {
        BillingService stripeBill = new BillingService(new StripePayment());
        BillingService paypalBill = new BillingService(new PayPalPayment());
        System.out.println(stripeBill.charge(1200.00, "DX-1001"));
        System.out.println(paypalBill.charge(850.50, "DX-1002"));
    }
}
