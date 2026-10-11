# Java strategy

From this folder:

```
javac StrategyDemo.java
java StrategyDemo
```

The program prints a Stripe charge for `DX-1001` and a PayPal charge for `DX-1002`. `BillingService` does not choose the provider itself. Neither class calls a payment API.
