/**
 * PART 2 — EVOLUTION 2: KITCHEN WORKFLOW (KDS Station Routing)
 *
 * Shows how the Observer pattern is EXTENDED to route order items
 * to specific kitchen stations (Cold, Hot, Bar) instead of one room.
 *
 * Run: node evolution2_kitchen_workflow.js
 */

// ─────────────────────────────────────────
// EventBus — same as Part 1 Observer demo
// ─────────────────────────────────────────
class EventBus {
  constructor() { this._rooms = new Map(); }

  subscribe(room, name, cb) {
    if (!this._rooms.has(room)) this._rooms.set(room, []);
    this._rooms.get(room).push({ name, cb });
    console.log(`  [EventBus] '${name}' subscribed to '${room}'`);
  }

  emit(room, event, data) {
    const observers = this._rooms.get(room) || [];
    for (const o of observers) o.cb(event, data);
  }
}

// ─────────────────────────────────────────
// BEFORE — one kitchen room, all items broadcast to same screen
// ─────────────────────────────────────────
class KitchenServiceBefore {
  constructor(bus, restaurantId) { this._bus = bus; this._rid = restaurantId; }

  notifyKitchen(order) {
    console.log(`\n  [KitchenService-BEFORE] Broadcasting ALL items to single kitchen room`);
    this._bus.emit(`restaurant:${this._rid}:kitchen`, 'kitchen:order:new', order);
  }
}

// ─────────────────────────────────────────
// AFTER — route items to station-specific rooms
// ─────────────────────────────────────────
const STATION_MAP = {
  APPETIZER: 'cold', SALAD: 'cold', SOUP: 'cold',
  ENTREE: 'hot',    SIDE: 'hot',
  DESSERT: 'bar',   BEVERAGE: 'bar',
};

class KitchenServiceAfter {
  constructor(bus, restaurantId) { this._bus = bus; this._rid = restaurantId; }

  notifyKitchen(order) {
    console.log(`\n  [KitchenService-AFTER] Routing items to correct stations...`);
    for (const item of order.items) {
      const station = STATION_MAP[item.courseType] || 'hot'; // default hot
      const room = `restaurant:${this._rid}:kitchen:${station}`;
      this._bus.emit(room, 'kitchen:order:new', { orderId: order.id, item });
    }
  }
}

// ─────────────────────────────────────────
// Observer callbacks (simulated kitchen screens)
// ─────────────────────────────────────────
const singleKitchenScreen  = (event, data) => console.log(`    [SingleKitchenScreen] → ${event}:`, data);
const coldStationScreen    = (event, data) => console.log(`    [ColdStation 🧊]       → ${event}:`, data);
const hotStationScreen     = (event, data) => console.log(`    [HotStation  🔥]       → ${event}:`, data);
const barStationScreen     = (event, data) => console.log(`    [BarStation  🍹]       → ${event}:`, data);

// ─────────────────────────────────────────
// Demo
// ─────────────────────────────────────────
const RID = 'rest_001';
const bus = new EventBus();

console.log('\n===== EVOLUTION 2: KITCHEN WORKFLOW (KDS Station Routing) =====\n');

// BEFORE setup
const kitchenBefore = new KitchenServiceBefore(bus, RID);
bus.subscribe(`restaurant:${RID}:kitchen`, 'SingleKitchenScreen', singleKitchenScreen);

// AFTER setup
const kitchenAfter = new KitchenServiceAfter(bus, RID);
bus.subscribe(`restaurant:${RID}:kitchen:cold`, 'ColdStation', coldStationScreen);
bus.subscribe(`restaurant:${RID}:kitchen:hot`,  'HotStation',  hotStationScreen);
bus.subscribe(`restaurant:${RID}:kitchen:bar`,  'BarStation',  barStationScreen);

const sampleOrder = {
  id: 'ord_001',
  items: [
    { name: 'Caesar Salad', courseType: 'SALAD' },
    { name: 'Grilled Salmon', courseType: 'ENTREE' },
    { name: 'Garlic Bread', courseType: 'APPETIZER' },
    { name: 'Chocolate Mousse', courseType: 'DESSERT' },
  ]
};

console.log('\n--- BEFORE: All items → one kitchen room ---');
kitchenBefore.notifyKitchen(sampleOrder);

console.log('\n--- AFTER: Items routed by course type to stations ---');
kitchenAfter.notifyKitchen(sampleOrder);
