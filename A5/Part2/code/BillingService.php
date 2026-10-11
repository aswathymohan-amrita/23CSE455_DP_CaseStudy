<?php

// Proposed Part 2 code. The runnable versions are in Part3/strategy.

interface PaymentStrategy
{
    public function processPayment(float $amount, string $reference): array;
}

class BillingService
{
    public function __construct(private PaymentStrategy $strategy)
    {
    }

    public function charge(float $amount, string $reference): array
    {
        return $this->strategy->processPayment($amount, $reference);
    }
}
