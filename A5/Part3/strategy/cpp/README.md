# C++ strategy

From this folder:

```
g++ -std=c++17 strategy_demo.cpp -o strategy_demo
./strategy_demo
```

On Windows the program file is `strategy_demo.exe`. It prints the Stripe line and the PayPal line, and exits with code 1 if a provider name is wrong. Neither class calls a payment API.
