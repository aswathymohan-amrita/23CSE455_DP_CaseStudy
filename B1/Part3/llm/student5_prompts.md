# Student 5: LLM Prompts & Chat History Record

**Student Name:** `[Enter Student 5 Name]`  
**Roll Number:** `[Enter Roll Number]`  
**Assigned Design Patterns:** **Command** (Behavioral) & **Template Method** (Behavioral)  
**Public Chat History Link:** `[PASTE CHAT LINK HERE: e.g., https://chatgpt.com/share/xxxx or https://gemini.google.com/share/xxxx]`  
**Date:** `09-10-2026`  
**LLM Model Used:** `Gemini 2.5 Flash / Claude 3.5 Sonnet / ChatGPT-4o`  

---

## Instructions for Student 5
1. Open [ChatGPT](https://chatgpt.com), [Claude](https://claude.ai), or [Gemini](https://gemini.google.com).
2. Start a **new chat**.
3. Copy and paste **Prompt 1 (Command)** and let the model generate the code and explanation.
4. In the **same chat**, copy and paste **Prompt 2 (Template Method)**.
5. Click **Share** / **Export Chat** and generate a public link.
6. Paste your public link above at `Public Chat History Link`.

---

## Prompt 1: Command Pattern (Software Evolution 3 & Cross-Language Implementation)

### Copy and Paste this into the LLM:
```text
We are working on a 23CSE455 Design Patterns case study for a Restaurant Management and Point of Sale (POS) System.

I am responsible for the Command Pattern under Software Evolution 3 (POS Terminal Cashier Actions & Multi-Level Undo).

When cashiers build orders on a touchscreen terminal, mistakes happen (e.g., adding the wrong item, or applying an erroneous promotional discount). The system must allow cashiers to hit an "Undo" button to reverse operations cleanly, while logging each action in an audit trail.

Please do the following:
1. Explain how the GoF Command Pattern encapsulates cashier operations into executable objects with `execute()` and `undo()` capabilities.
2. Define the `POSCommand` interface with `execute()` and `undo()`.
3. Implement `CartReceiver` that tracks cart items, item prices, and running subtotal.
4. Implement concrete command classes:
   - `AddItemCommand(receiver, itemName, price)`
   - `ApplyDiscountCommand(receiver, discountDollars)`
5. Implement `POSTerminalInvoker` holding an execution history stack to support multi-step undo.
6. Provide complete, runnable implementations of this Command pattern across 4 programming languages: Java, Python, JavaScript (Node.js), and C++.
7. Demonstrate:
   - Adding "Truffle Pasta" ($24.00)
   - Adding "House Red Wine" ($11.00)
   - Applying a $5.00 VIP Coupon (Subtotal: $30.00)
   - Triggering Undo twice: first undoing the discount ($35.00), then undoing the wine ($24.00).
```

---

## Prompt 2: Template Method Pattern (Software Evolution 3 & Cross-Language Implementation)

### Copy and Paste this into the LLM:
```text
In the same Restaurant POS system, I am responsible for the Template Method Pattern under Software Evolution 3 (Order Fulfillment Pipeline Standardization).

Every order in the restaurant must follow an invariant 4-step execution lifecycle:
Step 1: Validate Order (Check ingredient inventory & kitchen capacity) — COMMON to all orders.
Step 2: Calculate Total (Apply taxes, delivery fees, or packaging surcharges) — HOOK (varies by channel).
Step 3: Send Kitchen Ticket (Dispatch to physical printer or KDS display) — COMMON to all orders.
Step 4: Notify Customer (Display on waiter tablet vs. send SMS courier link) — HOOK (varies by channel).

Please do the following:
1. Explain how the Template Method pattern defines the invariant algorithm skeleton in a base class while letting subclasses override specific steps without changing the overall structure.
2. Define the base class `OrderProcessingPipeline` with the template method `processOrder(orderId, subtotal)` and abstract hook methods.
3. Implement `DineInPipeline`:
   - Calculates 8.25% dine-in tax with no delivery fee.
   - Notifies the customer via the table's waiter console.
4. Implement `OnlineDeliveryPipeline`:
   - Calculates 8.25% tax + $4.99 delivery fee.
   - Notifies the customer by sending an SMS tracking link to the courier en route.
5. Provide complete, runnable implementations of this Template Method pattern across 4 programming languages: Java, Python, JavaScript (Node.js), and C++.
6. Demonstrate running both Dine-In and Delivery orders through the template pipeline.
```

---

## Human Verification Checklist
- [x] Command tested in Java (`Part3/command/CommandDemo.java`) & captured in `data/test_result/command_java.txt`
- [x] Command tested in Python (`Part3/command/CommandDemo.py`) & captured in `data/test_result/command_python.txt`
- [x] Command tested in JavaScript (`Part3/command/CommandDemo.js`) & captured in `data/test_result/command_js.txt`
- [x] Command tested in C++ (`Part3/command/CommandDemo.cpp`) & captured in `data/test_result/command_cpp.txt`
- [x] Template Method tested in Java, Python, JS, C++ & captured in `data/test_result/template_*.txt`
