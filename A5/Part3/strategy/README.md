# Strategy

`BillingService` keeps a `PaymentStrategy` and calls it. `StripePayment` and `PayPalPayment` are the two implementations. The service does not contain a branch on the provider name.

| Language | Folder | Command |
|---|---|---|
| Java | `java/` | `javac StrategyDemo.java` then `java StrategyDemo` |
| Python | `python/` | `python strategy_demo.py` |
| JavaScript | `javascript/` | `node strategyDemo.js` |
| C++ | `cpp/` | `g++ -std=c++17 strategy_demo.cpp -o strategy_demo` |

A correct run prints `stripe` for `DX-1001` and `paypal` for `DX-1002`. JavaScript and C++ exit with code 1 if the provider name is wrong. `pattern_crosslanguage.csv` compares the four versions. The prompt is in `llm/part3_prompt.txt`.
