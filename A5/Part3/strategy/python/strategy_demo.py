"""Part 3 - Strategy demonstration (Python).

BillingService is the context. Stripe and PayPal are simulated strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float, reference: str) -> dict[str, str | float]:
        raise NotImplementedError


class StripePayment(PaymentStrategy):
    def process_payment(self, amount: float, reference: str) -> dict[str, str | float]:
        return {
            "provider": "stripe",
            "reference": reference,
            "amount": amount,
            "status": "paid",
        }


class PayPalPayment(PaymentStrategy):
    def process_payment(self, amount: float, reference: str) -> dict[str, str | float]:
        return {
            "provider": "paypal",
            "reference": reference,
            "amount": amount,
            "status": "paid",
        }


class BillingService:
    def __init__(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    def charge(self, amount: float, reference: str) -> dict[str, str | float]:
        return self._strategy.process_payment(amount, reference)


if __name__ == "__main__":
    stripe_bill = BillingService(StripePayment())
    paypal_bill = BillingService(PayPalPayment())
    print(stripe_bill.charge(1200.00, "DX-1001"))
    print(paypal_bill.charge(850.50, "DX-1002"))
