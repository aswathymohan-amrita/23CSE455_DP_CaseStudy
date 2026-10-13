# Student 3: LLM Prompts & Chat History Record

**Student Name:** `[Enter Student 3 Name]`  
**Roll Number:** `[Enter Roll Number]`  
**Assigned Design Patterns:** **Adapter** (Structural) & **State** (Behavioral)  
**Public Chat History Link:** `[PASTE CHAT LINK HERE: e.g., https://chatgpt.com/share/xxxx or https://gemini.google.com/share/xxxx]`  
**Date:** `09-10-2026`  
**LLM Model Used:** `Gemini 2.5 Flash / Claude 3.5 Sonnet / ChatGPT-4o`  

---

## Instructions for Student 3
1. Open [ChatGPT](https://chatgpt.com), [Claude](https://claude.ai), or [Gemini](https://gemini.google.com).
2. Start a **new chat**.
3. Copy and paste **Prompt 1 (Adapter)** and let the model generate the code and explanation.
4. In the **same chat**, copy and paste **Prompt 2 (State)**.
5. Click **Share** / **Export Chat** and generate a public link.
6. Paste your public link above at `Public Chat History Link`.

---

## Prompt 1: Adapter Pattern (Software Evolution 1 & Cross-Language Implementation)

### Copy and Paste this into the LLM:
```text
We are working on a 23CSE455 Design Patterns case study for a Restaurant Management and Point of Sale (POS) System.

I am responsible for the Adapter Pattern under Software Evolution 1 (Online Ordering Integration). Our POS backend requires orders in a standard internal domain format: `POSOrder(orderId, customerName, totalAmount, deliveryAddress)`.

However, third-party delivery platforms send heterogeneous JSON payloads:
1. DoorDash sends: `{ "delivery_id": "DD-101", "recipient": { "full_name": "Alice Green", "dropoff_location": "742 Evergreen Terrace" }, "order_total_cents": 3450 }`.
2. UberEats sends: `{ "eats_order_ref": "UBER-909", "client_info": { "name": "Bob Vance", "destination_address": "100 Industrial Pkwy" }, "cart_total_usd": 28.75 }`.

Please do the following:
1. Explain how the Object Adapter pattern allows our system to ingest external vendor orders without modifying our core POSOrder structure.
2. Define the Target interface `DeliveryOrderAdapter` with a method `toPOSOrder()`.
3. Implement `DoorDashAdapter` and `UberEatsAdapter` that adapt their respective third-party formats.
4. Provide complete, runnable implementations of this exact Adapter pattern across 4 programming languages: Java, Python, JavaScript (Node.js), and C++.
5. The output should print normalized POS orders showing Order ID, Customer Name, Total, and Address for both DoorDash and UberEats.
```

---

## Prompt 2: State Pattern (Software Evolution 2 & Cross-Language Implementation)

### Copy and Paste this into the LLM:
```text
In the same Restaurant POS system, I am responsible for the State Pattern under Software Evolution 2 (Dining Floor & Table Lifecycle Management).

In a restaurant, dining tables follow a strict operational lifecycle:
1. AVAILABLE: Waiting for guests. Can be seated (moves to OCCUPIED). Cannot order or pay.
2. OCCUPIED: Guests are seated. Can place orders (moves to ORDER_PLACED).
3. ORDER_PLACED: Food ordered / dining. Can request bill (moves to BILLED).
4. BILLED: Bill paid. Can be cleaned and freed (moves back to AVAILABLE).

Please do the following:
1. Explain how the GoF State Pattern replaces messy if/else state checks and prevents illegal operations (e.g. attempting to pay a bill on an empty table).
2. Define a TableState interface/abstract class with methods: `seatGuests()`, `placeOrder()`, `requestBill()`, and `clearTable()`.
3. Implement concrete state classes: AvailableState, OccupiedState, OrderPlacedState, and BilledState.
4. Implement TableContext managing the current state and table number.
5. Provide complete, runnable implementations of this State pattern across 4 programming languages: Java, Python, JavaScript (Node.js), and C++.
6. Demonstrate both valid sequential transitions for Table #5 and an invalid transition attempt.
```

---

## Human Verification Checklist
- [x] Adapter tested in Java (`Part3/adapter/AdapterDemo.java`) & captured in `data/test_result/adapter_java.txt`
- [x] Adapter tested in Python (`Part3/adapter/AdapterDemo.py`) & captured in `data/test_result/adapter_python.txt`
- [x] Adapter tested in JavaScript (`Part3/adapter/AdapterDemo.js`) & captured in `data/test_result/adapter_js.txt`
- [x] Adapter tested in C++ (`Part3/adapter/AdapterDemo.cpp`) & captured in `data/test_result/adapter_cpp.txt`
- [x] State tested in Java, Python, JS, C++ & captured in `data/test_result/state_*.txt`
