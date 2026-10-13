from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        pass

class CashPayment(PaymentStrategy):
    def __init__(self, tendered: float):
        self.tendered = tendered

    def process_payment(self, amount: float) -> str:
        if self.tendered < amount:
            return f"FAILED: Tendered ${self.tendered} < Total ${amount}"
        change = self.tendered - amount
        return f"SUCCESS [CASH]: Paid ${amount:.2f} | Change due: ${change:.2f}"

class StripeCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def process_payment(self, amount: float) -> str:
        last4 = self.card_number[-4:]
        return f"SUCCESS [STRIPE]: Charged ${amount:.2f} to card ending in {last4} (tx_stripe_9821)"

class MobilePayPayment(PaymentStrategy):
    def __init__(self, provider: str):
        self.provider = provider

    def process_payment(self, amount: float) -> str:
        return f"SUCCESS [MOBILE]: Authorized ${amount:.2f} via {self.provider} (ref_qr_5541)"

class CheckoutContext:
    def __init__(self, strategy: PaymentStrategy = None):
        self.strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def checkout(self, amount: float) -> str:
        if not self.strategy:
            return "FAILED: No payment strategy set"
        return self.strategy.process_payment(amount)

if __name__ == "__main__":
    checkout = CheckoutContext()
    order_total = 42.50

    checkout.set_strategy(StripeCardPayment("4242-4242-4242-1234"))
    print("Test 1 - Stripe:", checkout.checkout(order_total))

    checkout.set_strategy(CashPayment(50.00))
    print("Test 2 - Cash:  ", checkout.checkout(order_total))

    checkout.set_strategy(MobilePayPayment("ApplePay"))
    print("Test 3 - Mobile:", checkout.checkout(order_total))
