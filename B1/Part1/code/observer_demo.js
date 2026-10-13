/**
 * PART 1 — OBSERVER PATTERN DEMO
 * Mirrors the exact structure found in:
 *   src/websocket.ts            (setupWebSocket — Subject/Publisher)
 *   src/services/order.service.ts  (io.emit — Publisher)
 *   Frontend socket.io listeners   (Observers/Subscribers)
 *
 * Run: node observer_demo.js
 */

// ─────────────────────────────────────────
// SUBJECT — EventBus  (≈ Socket.IO Server)
// ─────────────────────────────────────────
class EventBus {
  constructor() {
    this._rooms = new Map();   // room name → Set of observer callbacks
  }

  /** Observer joins a room  (≈ socket.join) */
  subscribe(room, observerName, callback) {
    if (!this._rooms.has(room)) this._rooms.set(room, []);
    this._rooms.get(room).push({ name: observerName, callback });
    console.log(`  [EventBus] '${observerName}' subscribed to room '${room}'`);
  }

  /** Publisher broadcasts to all observers in a room  (≈ io.to(room).emit) */
  emit(room, event, data) {
    console.log(`\n  [EventBus] Broadcasting '${event}' → room '${room}'`);
    const observers = this._rooms.get(room) || [];
    if (observers.length === 0) console.log('    (no observers in this room)');
    for (const obs of observers) {
      obs.callback(event, data);
    }
  }
}

// ─────────────────────────────────────────
// PUBLISHER — OrderService  (≈ order.service.ts)
// ─────────────────────────────────────────
class OrderService {
  constructor(eventBus) { this._bus = eventBus; }

  createOrder(restaurantId, orderData) {
    const order = { id: `ord_${Date.now()}`, ...orderData, status: 'OPEN' };
    console.log(`\n  [OrderService] Order ${order.id} created — notifying observers...`);
    // Notify ALL floor clients
    this._bus.emit(`restaurant:${restaurantId}`, 'order:new', order);
    // Notify KITCHEN only
    this._bus.emit(`restaurant:${restaurantId}:kitchen`, 'kitchen:order:new', order);
    return order;
  }
}

// ─────────────────────────────────────────
// PUBLISHER — InventoryService
// ─────────────────────────────────────────
class InventoryService {
  constructor(eventBus) { this._bus = eventBus; }

  adjustStock(restaurantId, item, newQty) {
    if (newQty < item.reorderPoint) {
      console.log(`\n  [InventoryService] LOW STOCK triggered for '${item.name}' — alerting...`);
      this._bus.emit(`restaurant:${restaurantId}`, 'inventory:alert', {
        itemId: item.id, name: item.name, quantity: newQty, reorderPoint: item.reorderPoint
      });
    }
  }
}

// ─────────────────────────────────────────
// OBSERVERS — Frontend client screens
// ─────────────────────────────────────────
function kitchenScreenObserver(event, data) {
  console.log(`    [KitchenScreen]    received '${event}':`, data);
}
function floorTabletObserver(event, data) {
  console.log(`    [FloorTablet]      received '${event}':`, data);
}
function adminDashboardObserver(event, data) {
  console.log(`    [AdminDashboard]   received '${event}':`, data);
}

// ─────────────────────────────────────────
// BOOTSTRAP — Wire observers to rooms (≈ websocket.ts setup)
// ─────────────────────────────────────────
const RESTAURANT_ID = 'rest_001';
const bus           = new EventBus();
const orderService  = new OrderService(bus);
const inventorySvc  = new InventoryService(bus);

console.log('\n===== OBSERVER PATTERN DEMO (mirrors websocket.ts) =====\n');
console.log('-- Registering Observers --');
// Floor tablet and admin subscribe to main restaurant room
bus.subscribe(`restaurant:${RESTAURANT_ID}`, 'FloorTablet1', floorTabletObserver);
bus.subscribe(`restaurant:${RESTAURANT_ID}`, 'AdminDashboard', adminDashboardObserver);
// Kitchen screen subscribes to kitchen-only room
bus.subscribe(`restaurant:${RESTAURANT_ID}:kitchen`, 'KitchenScreen1', kitchenScreenObserver);

// ─────────────────────────────────────────
// EVENTS — Publishers fire; observers react
// ─────────────────────────────────────────
console.log('\n-- Event 1: New Order Created --');
orderService.createOrder(RESTAURANT_ID, {
  tableId: 'tbl_5', items: [{ name: 'Burger', qty: 2 }, { name: 'Fries', qty: 2 }]
});

console.log('\n-- Event 2: Inventory Low Stock --');
inventorySvc.adjustStock(RESTAURANT_ID,
  { id: 'inv_3', name: 'Tomatoes', reorderPoint: 10 },
  newQty = 6
);
