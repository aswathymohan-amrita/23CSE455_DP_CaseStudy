import java.util.*;

interface PaymentStrategy {
    String processPayment(double amount);
}

class CashPayment implements PaymentStrategy {
    private double tendered;
    public CashPayment(double tendered) { this.tendered = tendered; }
    public String processPayment(double amount) {
        if (tendered < amount) return "FAILED: Tendered $" + tendered + " < Total $" + amount;
        double change = tendered - amount;
        return "SUCCESS [CASH]: Paid $" + amount + " | Change due: $" + String.format("%.2f", change);
    }
}

class StripeCardPayment implements PaymentStrategy {
    private String cardNumber;
    public StripeCardPayment(String cardNumber) { this.cardNumber = cardNumber; }
    public String processPayment(double amount) {
        String last4 = cardNumber.substring(Math.max(0, cardNumber.length() - 4));
        return "SUCCESS [STRIPE]: Charged $" + amount + " to card ending in " + last4 + " (tx_stripe_9821)";
    }
}

class MobilePayPayment implements PaymentStrategy {
    private String provider;
    public MobilePayPayment(String provider) { this.provider = provider; }
    public String processPayment(double amount) {
        return "SUCCESS [MOBILE]: Authorized $" + amount + " via " + provider + " (ref_qr_5541)";
    }
}

class CheckoutContext {
    private PaymentStrategy strategy;
    public void setStrategy(PaymentStrategy strategy) { this.strategy = strategy; }
    public String checkout(double amount) {
        if (strategy == null) return "FAILED: No payment strategy set";
        return strategy.processPayment(amount);
    }
}

public class StrategyDemo {
    public static void main(String[] args) {
        CheckoutContext checkout = new CheckoutContext();
        double orderTotal = 42.50;

        checkout.setStrategy(new StripeCardPayment("4242-4242-4242-1234"));
        System.out.println("Test 1 - Stripe: " + checkout.checkout(orderTotal));

        checkout.setStrategy(new CashPayment(50.00));
        System.out.println("Test 2 - Cash:   " + checkout.checkout(orderTotal));

        checkout.setStrategy(new MobilePayPayment("ApplePay"));
        System.out.println("Test 3 - Mobile: " + checkout.checkout(orderTotal));
    }
}
