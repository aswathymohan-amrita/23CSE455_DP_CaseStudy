# Student 4: LLM Prompts & Chat History Record

**Student Name:** `[Enter Student 4 Name]`  
**Roll Number:** `[Enter Roll Number]`  
**Assigned Design Patterns:** **Factory Method** (Creational) & **Decorator** (Structural)  
**Public Chat History Link:** `[PASTE CHAT LINK HERE: e.g., https://chatgpt.com/share/xxxx or https://gemini.google.com/share/xxxx]`  
**Date:** `09-10-2026`  
**LLM Model Used:** `Gemini 2.5 Flash / Claude 3.5 Sonnet / ChatGPT-4o`  

---

## Instructions for Student 4
1. Open [ChatGPT](https://chatgpt.com), [Claude](https://claude.ai), or [Gemini](https://gemini.google.com).
2. Start a **new chat**.
3. Copy and paste **Prompt 1 (Factory Method)** and let the model generate the code and explanation.
4. In the **same chat**, copy and paste **Prompt 2 (Decorator)**.
5. Click **Share** / **Export Chat** and generate a public link.
6. Paste your public link above at `Public Chat History Link`.

---

## Prompt 1: Factory Method Pattern (Software Evolution 1 & Cross-Language Implementation)

### Copy and Paste this into the LLM:
```text
We are working on a 23CSE455 Design Patterns case study for a Restaurant Management and Point of Sale (POS) System.

I am responsible for the Factory Method Pattern under Software Evolution 1 (Multi-Channel Kitchen Tickets). In the baseline system, only dine-in orders existed. With online ordering added, the kitchen requires different physical ticket formats:
1. DineInTicket: displays Table Number, Server Name, and prints "SERVE ON CERAMIC PLATES".
2. TakeoutTicket: displays Pickup Time, Customer Phone, and prints "PACK IN BROWN PAPER BAG WITH NAPKINS".
3. DeliveryTicket: displays Delivery Address, Courier Name, and prints "SEAL IN THERMAL INSULATED BAG WITH TAMPER TAPE".

Please do the following:
1. Explain how the Factory Method pattern decouples the order intake system from concrete ticket printing classes.
2. Define a KitchenTicket interface/abstract class with a `printTicket()` method.
3. Define concrete ticket products: DineInTicket, TakeoutTicket, and DeliveryTicket.
4. Define the TicketCreator / TicketFactory base class with the abstract factory method `createTicket(orderId, details)`.
5. Provide complete, runnable implementations of this Factory Method pattern across 4 programming languages: Java, Python, JavaScript (Node.js), and C++.
6. Demonstrate creating tickets for all 3 channels in the main test runner.
```

---

## Prompt 2: Decorator Pattern (Software Evolution 2 & Cross-Language Implementation)

### Copy and Paste this into the LLM:
```text
In the same Restaurant POS system, I am responsible for the Decorator Pattern under Software Evolution 2 (Menu Item Customization & Prep Notes).

Customers regularly modify food items with add-ons:
1. Base item: Gourmet Burger ($12.00)
2. Add Extra Aged Cheddar Cheese (+ $1.50, prep note: "[Extra Melted Cheese]")
3. Add Crispy Smoked Bacon (+ $2.25, prep note: "[Double Smoked Bacon]")
4. Add Gluten-Free Brioche Bun (+ $2.00, prep note: "[ALLERGEN: Gluten-Free Prep Station]")

If implemented using inheritance, every combination would cause a class explosion (BurgerWithCheese, BurgerWithCheeseAndBacon, etc.).

Please do the following:
1. Explain how the GoF Decorator Pattern allows dynamic composition of price additions and preparation notes at runtime.
2. Define the MenuItem component interface with `getDescription()`, `getCost()`, and `getPrepNotes()`.
3. Implement concrete component `Burger` and the abstract `MenuItemDecorator`.
4. Implement concrete decorators: `ExtraCheese`, `CrispyBacon`, and `GlutenFree`.
5. Provide complete, runnable implementations of this Decorator pattern across 4 programming languages: Java, Python, JavaScript (Node.js), and C++.
6. Demonstrate building a base burger, adding cheese, adding bacon, and adding a gluten-free bun, showing the compound price calculation ($17.75) and combined prep notes.
```

---

## Human Verification Checklist
- [x] Factory Method tested in Java (`Part3/factory/FactoryDemo.java`) & captured in `data/test_result/factory_java.txt`
- [x] Factory Method tested in Python (`Part3/factory/FactoryDemo.py`) & captured in `data/test_result/factory_python.txt`
- [x] Factory Method tested in JavaScript (`Part3/factory/FactoryDemo.js`) & captured in `data/test_result/factory_js.txt`
- [x] Factory Method tested in C++ (`Part3/factory/FactoryDemo.cpp`) & captured in `data/test_result/factory_cpp.txt`
- [x] Decorator tested in Java, Python, JS, C++ & captured in `data/test_result/decorator_*.txt`
