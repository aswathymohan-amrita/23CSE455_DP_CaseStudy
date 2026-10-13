# Student 2: LLM Prompts & Chat History Record

**Student Name:** `[Enter Student 2 Name]`  
**Roll Number:** `[Enter Roll Number]`  
**Assigned Design Patterns:** **Strategy** (Behavioral) & **Observer** (Behavioral)  
**Public Chat History Link:** `[PASTE CHAT LINK HERE: e.g., https://chatgpt.com/share/xxxx or https://gemini.google.com/share/xxxx]`  
**Date:** `09-10-2026`  
**LLM Model Used:** `Gemini 2.5 Flash / Claude 3.5 Sonnet / ChatGPT-4o`  

---

## Instructions for Student 2
1. Open [ChatGPT](https://chatgpt.com), [Claude](https://claude.ai), or [Gemini](https://gemini.google.com).
2. Start a **new chat**.
3. Copy and paste **Prompt 1 (Strategy)** and let the model generate the code and explanation.
4. In the **same chat**, copy and paste **Prompt 2 (Observer)**.
5. Click **Share** / **Export Chat** and generate a public link.
6. Paste your public link above at `Public Chat History Link`.

---

## Prompt 1: Strategy Pattern (Software Evolution 3 & Cross-Language Implementation)

### Copy and Paste this into the LLM:
```text
We are working on a 23CSE455 Design Patterns case study for a Restaurant Management and Point of Sale (POS) System.

I am responsible for the Strategy Pattern under Software Evolution 3 (Multiple Payment Methods). In the baseline system, payment was handled as a plain database string ('CASH', 'CARD') with rigid conditional if/else blocks.

We need to refactor this using the GoF Strategy Pattern so new payment gateways (Stripe, ApplePay/QR, GiftCard) can be registered without modifying the payment execution core.

Please do the following:
1. Define an IPaymentStrategy interface with a method `pay(amount)`.
2. Implement 4 concrete strategies:
   - CashStrategy: accepts cash, validates tendered amount >= bill, and calculates change returned.
   - StripeCardStrategy: simulates card authorization and prints a Stripe transaction ID.
   - MobilePayStrategy: generates and verifies a QR payment token.
   - GiftCardStrategy: verifies pre-loaded balance and deducts the amount.
3. Provide a PaymentContext that holds the active strategy and executes transactions.
4. Provide complete, runnable implementations of this exact Strategy pattern across 4 programming languages: Java, Python, JavaScript (Node.js), and C++.
5. The test cases should demonstrate paying a $45.00 bill with Cash ($50 tendered -> $5.00 change) and a $30.00 bill via Stripe Card.
```

---

## Prompt 2: Observer Pattern (Software Evolution 2 & Cross-Language Implementation)

### Copy and Paste this into the LLM:
```text
In the same Restaurant POS system, I am responsible for the Observer Pattern under Software Evolution 2 (Kitchen Display System Station Workflow).

The baseline system had a single monolithic WebSocket emitter broadcasting 'order:new' to every screen. In our evolution, the kitchen is divided into specialized preparation stations:
1. Cold Station: prepares Salads, Sushi, and Cold Appetizers.
2. Hot Station: prepares Steaks, Pizzas, and Burgers.
3. Waiter Terminal: tracks when items are ready for pickup.

Please do the following:
1. Explain how the Observer pattern decouples the Order subject from the various station displays.
2. Define a KitchenObserver / StationObserver interface with an `update(ticket)` method.
3. Create concrete observers: ColdStationSubscriber, HotStationSubscriber, and WaiterTerminalSubscriber.
4. Implement the KitchenSubject that routes items to the matching station based on item metadata.
5. Provide complete, runnable implementations of this Observer pattern across 4 programming languages: Java, Python, JavaScript (Node.js), and C++.
6. Demonstrate dispatching an order ticket containing both a "Caesar Salad" (routed to Cold Station) and a "Ribeye Steak" (routed to Hot Station).
```

---

## Human Verification Checklist
- [x] Strategy tested in Java (`Part3/strategy/StrategyDemo.java`) & captured in `data/test_result/strategy_java.txt`
- [x] Strategy tested in Python (`Part3/strategy/StrategyDemo.py`) & captured in `data/test_result/strategy_python.txt`
- [x] Strategy tested in JavaScript (`Part3/strategy/StrategyDemo.js`) & captured in `data/test_result/strategy_js.txt`
- [x] Strategy tested in C++ (`Part3/strategy/StrategyDemo.cpp`) & captured in `data/test_result/strategy_cpp.txt`
- [x] Observer tested in Java, Python, JS, C++ & captured in `data/test_result/observer_*.txt`
