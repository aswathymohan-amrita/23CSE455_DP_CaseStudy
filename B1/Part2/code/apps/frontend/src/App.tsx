import React, { useState } from 'react';
import { FloorPlanEditor } from './components/FloorPlanEditor';
import { MenuBrowser } from './components/MenuBrowser';
import { OrderCart } from './components/OrderCart';
import { KitchenDisplay } from './components/KitchenDisplay';
import { OnlineOrdering } from './components/OnlineOrdering';
import { AuthModal, UserSession } from './components/AuthModal';
import { PaymentModal, PaymentMethodType } from './components/PaymentModal';
import { Table, TableStatus, TableShape } from './types/table.types';
import { MenuCategory, MenuItem } from './types/menu.types';
import { Order, OrderStatus, OrderItemStatus } from './types/order.types';

// Mock Initial Tables
const initialTables: Table[] = [
  {
    id: 'tbl_1',
    number: '1',
    floorPlanId: 'fp_1',
    capacity: 2,
    minCapacity: 1,
    x: 60,
    y: 80,
    width: 90,
    height: 90,
    shape: TableShape.SQUARE,
    section: 'Main Dining',
    status: TableStatus.AVAILABLE,
    currentOrder: null,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'tbl_2',
    number: '2',
    floorPlanId: 'fp_1',
    capacity: 4,
    minCapacity: 2,
    x: 220,
    y: 80,
    width: 120,
    height: 90,
    shape: TableShape.RECTANGLE,
    section: 'Main Dining',
    status: TableStatus.OCCUPIED,
    currentOrder: 'ord_101',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'tbl_3',
    number: '3',
    floorPlanId: 'fp_1',
    capacity: 4,
    minCapacity: 2,
    x: 400,
    y: 80,
    width: 100,
    height: 100,
    shape: TableShape.CIRCLE,
    section: 'Main Dining',
    status: TableStatus.AVAILABLE,
    currentOrder: null,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'tbl_4',
    number: '4',
    floorPlanId: 'fp_1',
    capacity: 6,
    minCapacity: 4,
    x: 100,
    y: 260,
    width: 160,
    height: 100,
    shape: TableShape.BOOTH,
    section: 'Patio',
    status: TableStatus.RESERVED,
    currentOrder: null,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'tbl_5',
    number: '5',
    floorPlanId: 'fp_1',
    capacity: 2,
    minCapacity: 1,
    x: 340,
    y: 260,
    width: 90,
    height: 90,
    shape: TableShape.SQUARE,
    section: 'Patio',
    status: TableStatus.AVAILABLE,
    currentOrder: null,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
];

// Mock Initial Menu Categories & Items
const initialCategories: MenuCategory[] = [
  {
    id: 'cat_1',
    name: 'Appetizers & Starters',
    restaurantId: 'rest_001',
    sortOrder: 1,
    createdAt: new Date(),
    updatedAt: new Date(),
    items: [
      {
        id: 'item_1',
        name: 'Crispy Calamari',
        description: 'Tender squid rings served with spicy marinara dipping sauce',
        price: 14.5,
        categoryId: 'cat_1',
        preparationTime: 12,
        calories: 420,
        allergens: ['Seafood', 'Gluten'],
        isAvailable: true,
        sortOrder: 1,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
      {
        id: 'item_2',
        name: 'Truffle Garlic Bread',
        description: 'Toasted sourdough with roasted garlic butter and black truffle oil',
        price: 9.0,
        categoryId: 'cat_1',
        preparationTime: 8,
        calories: 310,
        allergens: ['Dairy', 'Gluten'],
        isAvailable: true,
        sortOrder: 2,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
      {
        id: 'item_3',
        name: 'Classic Caesar Salad',
        description: 'Crisp romaine, shaved parmigiano, sourdough croutons, creamy dressing',
        price: 12.0,
        categoryId: 'cat_1',
        preparationTime: 7,
        calories: 280,
        allergens: ['Dairy', 'Egg'],
        isAvailable: true,
        sortOrder: 3,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    ],
  },
  {
    id: 'cat_2',
    name: 'Main Courses',
    restaurantId: 'rest_001',
    sortOrder: 2,
    createdAt: new Date(),
    updatedAt: new Date(),
    items: [
      {
        id: 'item_4',
        name: 'Prime Ribeye Steak (12oz)',
        description: 'Pan-seared ribeye with rosemary garlic butter and truffle mash',
        price: 38.0,
        categoryId: 'cat_2',
        preparationTime: 22,
        calories: 890,
        allergens: ['Dairy'],
        isAvailable: true,
        sortOrder: 1,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
      {
        id: 'item_5',
        name: 'Pan-Roasted Atlantic Salmon',
        description: 'Crispy skin salmon with lemon asparagus and herb beurre blanc',
        price: 28.5,
        categoryId: 'cat_2',
        preparationTime: 18,
        calories: 620,
        allergens: ['Fish', 'Dairy'],
        isAvailable: true,
        sortOrder: 2,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
      {
        id: 'item_6',
        name: 'Artisan Mushroom Risotto',
        description: 'Arborio rice with wild forest mushrooms, parmigiano, and thyme',
        price: 22.0,
        categoryId: 'cat_2',
        preparationTime: 16,
        calories: 540,
        allergens: ['Dairy'],
        isAvailable: true,
        sortOrder: 3,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    ],
  },
  {
    id: 'cat_3',
    name: 'Beverages & Cocktails',
    restaurantId: 'rest_001',
    sortOrder: 3,
    createdAt: new Date(),
    updatedAt: new Date(),
    items: [
      {
        id: 'item_7',
        name: 'Smoked Old Fashioned',
        description: 'Bourbon, aromatic bitters, orange peel, charred oak wood smoke',
        price: 16.0,
        categoryId: 'cat_3',
        preparationTime: 5,
        calories: 180,
        allergens: [],
        isAvailable: true,
        sortOrder: 1,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
      {
        id: 'item_8',
        name: 'Fresh Passionfruit Lemonade',
        description: 'Hand-squeezed Meyer lemons with organic passionfruit puree',
        price: 6.5,
        categoryId: 'cat_3',
        preparationTime: 3,
        calories: 120,
        allergens: [],
        isAvailable: true,
        sortOrder: 2,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    ],
  },
  {
    id: 'cat_4',
    name: 'Desserts',
    restaurantId: 'rest_001',
    sortOrder: 4,
    createdAt: new Date(),
    updatedAt: new Date(),
    items: [
      {
        id: 'item_9',
        name: 'Molten Belgian Chocolate Cake',
        description: 'Warm dark chocolate center with Madagascar vanilla bean gelato',
        price: 11.0,
        categoryId: 'cat_4',
        preparationTime: 10,
        calories: 520,
        allergens: ['Dairy', 'Gluten', 'Egg'],
        isAvailable: true,
        sortOrder: 1,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    ],
  },
];

// Initial Active Orders
const initialOrders: Order[] = [
  {
    id: 'ord_101',
    tableId: 'tbl_2',
    table: { id: 'tbl_2', number: '2' },
    status: OrderStatus.IN_PROGRESS,
    createdAt: new Date(Date.now() - 12 * 60 * 1000),
    updatedAt: new Date(),
    items: [
      {
        id: 'oi_1',
        orderId: 'ord_101',
        menuItemId: 'item_4',
        menuItem: { id: 'item_4', name: 'Prime Ribeye Steak (12oz)', price: 38.0 },
        quantity: 1,
        status: OrderItemStatus.PREPARING,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
      {
        id: 'oi_2',
        orderId: 'ord_101',
        menuItemId: 'item_1',
        menuItem: { id: 'item_1', name: 'Crispy Calamari', price: 14.5 },
        quantity: 1,
        status: OrderItemStatus.READY,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
      {
        id: 'oi_3',
        orderId: 'ord_101',
        menuItemId: 'item_7',
        menuItem: { id: 'item_7', name: 'Smoked Old Fashioned', price: 16.0 },
        quantity: 2,
        status: OrderItemStatus.SERVED,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    ],
  },
];

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'floor' | 'pos' | 'online' | 'kds' | 'orders' | 'patterns'>('floor');
  const [tables, setTables] = useState<Table[]>(initialTables);
  const [selectedTable, setSelectedTable] = useState<Table>(initialTables[0]);
  const [categories] = useState<MenuCategory[]>(initialCategories);
  const [orders, setOrders] = useState<Order[]>(initialOrders);

  // Auth & Session State (Facade + Chain of Responsibility)
  const [userSession, setUserSession] = useState<UserSession>({
    email: 'mgr@restaurant.com',
    role: 'MANAGER',
    token: 'tok_bWdyQHJlc3_MANAGER',
  });
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  // Payment Strategy State (Part 2 - Evolution 3)
  const [checkoutOrder, setCheckoutOrder] = useState<Order | null>(null);
  const [isPaymentModalOpen, setIsPaymentModalOpen] = useState(false);

  // Live Pattern Activity Log
  const [latestPatternEvent, setLatestPatternEvent] = useState<{
    pattern: string;
    description: string;
    timestamp: string;
  }>({
    pattern: 'Façade Pattern',
    description: 'AuthFacade initialized system session with token credentials.',
    timestamp: new Date().toLocaleTimeString(),
  });

  // Active Draft Cart for selected table
  const [cart, setCart] = useState<Order>({
    id: `ord_${Date.now()}`,
    tableId: selectedTable.id,
    table: { id: selectedTable.id, number: selectedTable.number },
    status: OrderStatus.OPEN,
    items: [],
    createdAt: new Date(),
    updatedAt: new Date(),
  });

  // Table Selection
  const handleSelectTable = (table: Table) => {
    setSelectedTable(table);
    setCart((prev) => ({
      ...prev,
      tableId: table.id,
      table: { id: table.id, number: table.number },
    }));
  };

  // Add Item to Cart
  const handleAddToCart = (item: MenuItem, quantity: number) => {
    setCart((prev) => {
      const existing = prev.items.find((i) => i.menuItemId === item.id);
      if (existing) {
        return {
          ...prev,
          items: prev.items.map((i) =>
            i.menuItemId === item.id ? { ...i, quantity: i.quantity + quantity } : i
          ),
        };
      } else {
        const newItem = {
          id: `item_${Date.now()}_${Math.random().toString(36).substring(7)}`,
          orderId: prev.id,
          menuItemId: item.id,
          menuItem: {
            id: item.id,
            name: item.name,
            price: item.price,
            description: item.description,
            image: item.image,
          },
          quantity,
          status: OrderItemStatus.PENDING,
          createdAt: new Date(),
          updatedAt: new Date(),
        };
        return { ...prev, items: [...prev.items, newItem] };
      }
    });
  };

  const handleRemoveCartItem = (itemId: string) => {
    setCart((prev) => ({
      ...prev,
      items: prev.items.filter((i) => i.id !== itemId),
    }));
  };

  const handleUpdateCartQty = (itemId: string, quantity: number) => {
    if (quantity <= 0) return handleRemoveCartItem(itemId);
    setCart((prev) => ({
      ...prev,
      items: prev.items.map((i) => (i.id === itemId ? { ...i, quantity } : i)),
    }));
  };

  // Submit Order (POS -> KDS)
  const handleSubmitOrder = () => {
    if (cart.items.length === 0) return;
    const submittedOrder: Order = {
      ...cart,
      id: `ord_${Date.now().toString().slice(-4)}`,
      status: OrderStatus.IN_PROGRESS,
      createdAt: new Date(),
    };

    setOrders((prev) => [submittedOrder, ...prev]);

    // Update table status to OCCUPIED
    setTables((prev) =>
      prev.map((t) =>
        t.id === cart.tableId ? { ...t, status: TableStatus.OCCUPIED, currentOrder: submittedOrder.id } : t
      )
    );

    // Reset Cart
    setCart({
      id: `ord_${Date.now()}`,
      tableId: selectedTable.id,
      table: { id: selectedTable.id, number: selectedTable.number },
      status: OrderStatus.OPEN,
      items: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    });

    setLatestPatternEvent({
      pattern: 'Observer Pattern (Socket.IO)',
      description: `Dispatched order:new event to KitchenDisplay stations (Order #${submittedOrder.id})`,
      timestamp: new Date().toLocaleTimeString(),
    });

    alert(`Order #${submittedOrder.id} placed! Kitchen tickets dispatched.`);
    setActiveTab('kds');
  };

  // Place Online Order (Part 2 — Evolution 1)
  const handlePlaceOnlineOrder = (onlineOrder: Order) => {
    setOrders((prev) => [onlineOrder, ...prev]);
    setLatestPatternEvent({
      pattern: 'Evolution 1: Public Online Ordering',
      description: `Public customer bypasses staff token check; validation chain approved Order #${onlineOrder.id}`,
      timestamp: new Date().toLocaleTimeString(),
    });
  };

  // Kitchen Item Status Progression (Pending -> Preparing -> Ready -> Served)
  const handleKitchenItemStatusChange = (orderId: string, itemId: string, newStatus: OrderItemStatus) => {
    setOrders((prev) =>
      prev.map((ord) => {
        if (ord.id !== orderId) return ord;
        const updatedItems = ord.items.map((it) => (it.id === itemId ? { ...it, status: newStatus } : it));

        // Evaluate overall order status
        const allReadyOrServed = updatedItems.every(
          (it) => it.status === OrderItemStatus.READY || it.status === OrderItemStatus.SERVED
        );
        const allServed = updatedItems.every((it) => it.status === OrderItemStatus.SERVED);

        let overallStatus = ord.status;
        if (allServed) overallStatus = OrderStatus.COMPLETED;
        else if (allReadyOrServed) overallStatus = OrderStatus.READY;
        else overallStatus = OrderStatus.IN_PROGRESS;

        return { ...ord, items: updatedItems, status: overallStatus };
      })
    );

    setLatestPatternEvent({
      pattern: 'Observer Pattern & KDS',
      description: `Kitchen item ${itemId} transitioned to ${newStatus}. Broadcasted to waiter terminals.`,
      timestamp: new Date().toLocaleTimeString(),
    });
  };

  // Payment Execution (Part 2 — Evolution 3 Strategy Pattern)
  const handlePaymentSuccess = (orderId: string, method: PaymentMethodType, details: any) => {
    // Mark order as COMPLETED
    setOrders((prev) =>
      prev.map((ord) => (ord.id === orderId ? { ...ord, status: OrderStatus.COMPLETED } : ord))
    );

    // Free the table
    const targetOrder = orders.find((o) => o.id === orderId);
    if (targetOrder && targetOrder.tableId !== 'online') {
      setTables((prev) =>
        prev.map((t) =>
          t.id === targetOrder.tableId ? { ...t, status: TableStatus.AVAILABLE, currentOrder: null } : t
        )
      );
    }

    setLatestPatternEvent({
      pattern: `Strategy Pattern (${method})`,
      description: `Order #${orderId.slice(-6)} successfully settled via ${method}. Table status freed.`,
      timestamp: new Date().toLocaleTimeString(),
    });
  };

  return (
    <div className="app-container">
      {/* Top Header */}
      <header className="app-header">
        <div className="brand">
          <span className="brand-icon">🍽️</span>
          <div>
            <h1 className="brand-title">Saffron & Sage POS</h1>
            <p style={{ fontSize: '0.78rem', color: '#78716c' }}>Restaurant Design Patterns & Evolution Suite</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="nav-tabs">
          <button
            onClick={() => setActiveTab('floor')}
            className={`nav-tab ${activeTab === 'floor' ? 'active' : ''}`}
          >
            <span>🗺️</span> Floor Plan
          </button>
          <button
            onClick={() => setActiveTab('pos')}
            className={`nav-tab ${activeTab === 'pos' ? 'active' : ''}`}
          >
            <span>📝</span> POS Terminal (T#{selectedTable.number})
          </button>
          <button
            onClick={() => setActiveTab('online')}
            className={`nav-tab ${activeTab === 'online' ? 'active' : ''}`}
          >
            <span>🛵</span> Online Orders
          </button>
          <button
            onClick={() => setActiveTab('kds')}
            className={`nav-tab ${activeTab === 'kds' ? 'active' : ''}`}
          >
            <span>🍳</span> Kitchen Display (KDS)
          </button>
          <button
            onClick={() => setActiveTab('orders')}
            className={`nav-tab ${activeTab === 'orders' ? 'active' : ''}`}
          >
            <span>📋</span> Active Orders ({orders.filter((o) => o.status !== OrderStatus.COMPLETED).length})
          </button>
          <button
            onClick={() => setActiveTab('patterns')}
            className={`nav-tab ${activeTab === 'patterns' ? 'active' : ''}`}
          >
            <span>🧩</span> Pattern Console
          </button>
        </nav>

        {/* Staff Session Pill (Facade & CoR Trigger) */}
        <div className="header-right">
          <div className="staff-session-pill" onClick={() => setIsAuthModalOpen(true)} title="Click to test AuthFacade & CoR Middleware">
            <span>👤</span>
            <div>
              <strong style={{ fontSize: '0.8rem', display: 'block', lineHeight: 1.1 }}>{userSession.email.split('@')[0]}</strong>
              <span className="role-badge">{userSession.role}</span>
            </div>
            <span style={{ fontSize: '0.7rem', color: '#ea580c' }}>Switch &rarr;</span>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="app-main">
        {/* Live GoF Pattern Activity Toast / Banner */}
        <div className="pattern-activity-bar">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <span className="pill-badge orange">LIVE PATTERN DISPATCH</span>
            <strong>{latestPatternEvent.pattern}:</strong>
            <span style={{ color: '#44403c' }}>{latestPatternEvent.description}</span>
          </div>
          <span style={{ fontSize: '0.75rem', color: '#a8a29e' }}>⏱️ {latestPatternEvent.timestamp}</span>
        </div>

        {/* TAB 1: Floor Plan */}
        {activeTab === 'floor' && (
          <div>
            <div className="floor-plan-controls">
              <div>
                <h2 style={{ color: '#1c1917' }}>Restaurant Dining Room Floor Plan</h2>
                <p style={{ color: '#78716c', fontSize: '0.875rem' }}>
                  Click any table to open the order terminal. Drag to reposition tables in editor mode.
                </p>
              </div>
              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.85rem' }}>
                  <span style={{ width: 12, height: 12, background: '#10b981', borderRadius: '50%' }}></span> Available
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.85rem' }}>
                  <span style={{ width: 12, height: 12, background: '#ef4444', borderRadius: '50%' }}></span> Occupied
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.85rem' }}>
                  <span style={{ width: 12, height: 12, background: '#3b82f6', borderRadius: '50%' }}></span> Reserved
                </span>
              </div>
            </div>

            <FloorPlanEditor
              tables={tables}
              width={1000}
              height={520}
              onTableMove={(tableId, x, y) => {
                setTables((prev) => prev.map((t) => (t.id === tableId ? { ...t, x, y } : t)));
              }}
              onTableClick={(table) => {
                handleSelectTable(table);
                setActiveTab('pos');
              }}
              onTableCreate={(x, y) => {
                const newTable: Table = {
                  id: `tbl_${Date.now()}`,
                  number: `${tables.length + 1}`,
                  floorPlanId: 'fp_1',
                  capacity: 4,
                  minCapacity: 2,
                  x,
                  y,
                  width: 100,
                  height: 100,
                  shape: TableShape.SQUARE,
                  section: 'Main',
                  status: TableStatus.AVAILABLE,
                  currentOrder: null,
                  createdAt: new Date().toISOString(),
                  updatedAt: new Date().toISOString(),
                };
                setTables((prev) => [...prev, newTable]);
              }}
              editorMode="edit"
            />
          </div>
        )}

        {/* TAB 2: POS Menu & Cart */}
        {activeTab === 'pos' && (
          <div>
            <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h2 style={{ color: '#1c1917' }}>Table #{selectedTable.number} — Order Entry Terminal</h2>
                <p style={{ color: '#78716c', fontSize: '0.85rem' }}>
                  Section: {selectedTable.section} &bull; Capacity: {selectedTable.capacity} guests &bull; Status: {selectedTable.status}
                </p>
              </div>
              <button
                onClick={() => setActiveTab('floor')}
                style={{ background: '#f8f6f0', border: '1px solid #d6cfbf', padding: '0.45rem 1rem', borderRadius: 8, cursor: 'pointer', fontWeight: 600 }}
              >
                &larr; Switch Table
              </button>
            </div>

            <div className="pos-grid">
              <MenuBrowser categories={categories} onSelectItem={handleAddToCart} />
              <OrderCart
                order={cart}
                onRemoveItem={handleRemoveCartItem}
                onUpdateQuantity={handleUpdateCartQty}
                onSubmitOrder={handleSubmitOrder}
                onCancelOrder={() => setCart((prev) => ({ ...prev, items: [] }))}
              />
            </div>
          </div>
        )}

        {/* TAB 3: Online Customer Portal (Part 2 — Evolution 1) */}
        {activeTab === 'online' && (
          <OnlineOrdering
            categories={categories}
            onPlaceOnlineOrder={handlePlaceOnlineOrder}
          />
        )}

        {/* TAB 4: Kitchen Display System (Part 2 — Evolution 2) */}
        {activeTab === 'kds' && (
          <KitchenDisplay
            orders={orders}
            onItemStatusChange={handleKitchenItemStatusChange}
          />
        )}

        {/* TAB 5: Active Orders & Multi-Payment Checkout (Part 2 — Evolution 3) */}
        {activeTab === 'orders' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h2 style={{ color: '#1c1917' }}>Floor & Online Active Orders</h2>
                <p style={{ color: '#78716c', fontSize: '0.85rem' }}>
                  Click "Checkout & Pay" to test Strategy Pattern payment methods (Cash, Card, QR, Gift Card).
                </p>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '1.25rem' }}>
              {orders.length === 0 ? (
                <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '3rem', background: '#fff', borderRadius: 12, border: '1px solid #e7e2d9' }}>
                  <h3>No orders in system</h3>
                  <p style={{ color: '#78716c' }}>Create an order from Table POS or Online Ordering!</p>
                </div>
              ) : (
                orders.map((ord) => {
                  const subtotal = ord.items.reduce((s, it) => s + it.menuItem.price * it.quantity, 0);
                  const total = subtotal * 1.08;

                  return (
                    <div
                      key={ord.id}
                      style={{
                        background: '#ffffff',
                        border: '1px solid #e7e2d9',
                        borderRadius: 12,
                        padding: '1.25rem',
                        boxShadow: '0 2px 10px rgba(0,0,0,0.03)',
                        borderTop: ord.status === OrderStatus.COMPLETED ? '4px solid #16a34a' : '4px solid #ea580c',
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                        <div>
                          <span className="pill-badge orange" style={{ fontSize: '0.7rem' }}>
                            {ord.table ? `Table #${ord.table.number}` : 'Online Delivery'}
                          </span>
                          <h3 style={{ color: '#1c1917', fontSize: '1.1rem', marginTop: '0.2rem' }}>Order #{ord.id.slice(-6)}</h3>
                        </div>
                        <span
                          style={{
                            padding: '0.25rem 0.6rem',
                            borderRadius: 12,
                            fontSize: '0.75rem',
                            fontWeight: 700,
                            background: ord.status === OrderStatus.COMPLETED ? '#ecfdf5' : '#fff7ed',
                            color: ord.status === OrderStatus.COMPLETED ? '#15803d' : '#ea580c',
                            border: ord.status === OrderStatus.COMPLETED ? '1px solid #a7f3d0' : '1px solid #fed7aa',
                          }}
                        >
                          {ord.status}
                        </span>
                      </div>

                      {/* Items */}
                      <div style={{ maxHeight: 140, overflowY: 'auto', marginBottom: '0.75rem' }}>
                        {ord.items.map((it) => (
                          <div key={it.id} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', padding: '0.25rem 0' }}>
                            <span>
                              <strong>{it.quantity}x</strong> {it.menuItem.name}
                            </span>
                            <span style={{ fontSize: '0.75rem', color: it.status === OrderItemStatus.SERVED ? '#16a34a' : '#ea580c', fontWeight: 600 }}>
                              {it.status}
                            </span>
                          </div>
                        ))}
                      </div>

                      {/* Order Footer & Checkout */}
                      <div style={{ borderTop: '1px solid #f4efe6', paddingTop: '0.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                          <span style={{ fontSize: '0.75rem', color: '#78716c', display: 'block' }}>Total with Tax:</span>
                          <strong style={{ fontSize: '1.25rem', color: '#ea580c' }}>${total.toFixed(2)}</strong>
                        </div>

                        {ord.status !== OrderStatus.COMPLETED ? (
                          <button
                            onClick={() => {
                              setCheckoutOrder(ord);
                              setIsPaymentModalOpen(true);
                            }}
                            className="btn-primary-orange"
                            style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
                          >
                            💳 Pay & Settle Bill
                          </button>
                        ) : (
                          <span className="pill-badge green">PAID & CLOSED ✓</span>
                        )}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        )}

        {/* TAB 6: Pattern Console / Overview */}
        {activeTab === 'patterns' && (
          <div style={{ background: '#ffffff', borderRadius: 12, padding: '1.75rem', border: '1px solid #e7e2d9' }}>
            <h2 style={{ color: '#1c1917' }}>Design Pattern Architecture in this POS</h2>
            <p style={{ color: '#78716c', marginTop: '0.25rem', fontSize: '0.9rem' }}>
              Every feature you interact with in this frontend executes a corresponding Gang of Four (GoF) design pattern:
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem', marginTop: '1.5rem' }}>
              <div style={{ background: '#fdfbf7', border: '1px solid #fed7aa', borderRadius: 10, padding: '1.25rem' }}>
                <span className="pill-badge orange">Part 1 Confirmed — GoF</span>
                <h3 style={{ color: '#ea580c', marginTop: '0.35rem' }}>Façade Pattern</h3>
                <p style={{ fontSize: '0.85rem', color: '#44403c', marginTop: '0.5rem' }}>
                  <strong>Where:</strong> <code>AuthService.login()</code> & <code>OrderService.createOrder()</code>
                </p>
                <p style={{ fontSize: '0.8rem', color: '#78716c', marginTop: '0.4rem' }}>
                  Hides bcrypt hashing, JWT issuance, and database queries behind a single, clean API entry method. Try clicking your user profile in the top-right header to test the live simulator!
                </p>
              </div>

              <div style={{ background: '#fdfbf7', border: '1px solid #fed7aa', borderRadius: 10, padding: '1.25rem' }}>
                <span className="pill-badge orange">Part 1 Confirmed — GoF</span>
                <h3 style={{ color: '#ea580c', marginTop: '0.35rem' }}>Chain of Responsibility</h3>
                <p style={{ fontSize: '0.85rem', color: '#44403c', marginTop: '0.5rem' }}>
                  <strong>Where:</strong> <code>src/middleware/auth.ts</code> (Express middleware pipeline)
                </p>
                <p style={{ fontSize: '0.8rem', color: '#78716c', marginTop: '0.4rem' }}>
                  Requests pass sequentially through <code>TokenValidator</code> &rarr; <code>RoleChecker</code> &rarr; Handler. Any link can terminate the request with 401 or 403 or pass downstream.
                </p>
              </div>

              <div style={{ background: '#fdfbf7', border: '1px solid #fed7aa', borderRadius: 10, padding: '1.25rem' }}>
                <span className="pill-badge orange">Part 1 Confirmed — GoF</span>
                <h3 style={{ color: '#ea580c', marginTop: '0.35rem' }}>Observer Pattern</h3>
                <p style={{ fontSize: '0.85rem', color: '#44403c', marginTop: '0.5rem' }}>
                  <strong>Where:</strong> <code>websocket.ts</code> & Kitchen Display System (KDS)
                </p>
                <p style={{ fontSize: '0.8rem', color: '#78716c', marginTop: '0.4rem' }}>
                  Whenever orders or items change status, events (<code>kitchen:order:new</code>, <code>kitchen:item:completed</code>) are broadcasted to station subscribers in real-time.
                </p>
              </div>

              <div style={{ background: '#fff7ed', border: '1px solid #f97316', borderRadius: 10, padding: '1.25rem' }}>
                <span className="pill-badge orange">Part 2 — Evolution 3</span>
                <h3 style={{ color: '#c2410c', marginTop: '0.35rem' }}>Strategy Pattern</h3>
                <p style={{ fontSize: '0.85rem', color: '#44403c', marginTop: '0.5rem' }}>
                  <strong>Where:</strong> <code>PaymentService</code> (Checkout Modal)
                </p>
                <p style={{ fontSize: '0.8rem', color: '#78716c', marginTop: '0.4rem' }}>
                  Decouples payment algorithms (CashDrawer, StripeCard, MobilePay, GiftCard) behind a common <code>IPaymentStrategy</code> interface so new payment providers can be added without modifying the core POS service.
                </p>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Auth Modal (Facade + CoR) */}
      <AuthModal
        isOpen={isAuthModalOpen}
        currentSession={userSession}
        onLoginSuccess={(newSession) => {
          setUserSession(newSession);
          setLatestPatternEvent({
            pattern: 'Façade + Chain of Responsibility',
            description: `Switched session to ${newSession.email} (${newSession.role}) with valid JWT.`,
            timestamp: new Date().toLocaleTimeString(),
          });
        }}
        onClose={() => setIsAuthModalOpen(false)}
      />

      {/* Payment Modal (Strategy Pattern) */}
      <PaymentModal
        isOpen={isPaymentModalOpen}
        order={checkoutOrder}
        onClose={() => {
          setIsPaymentModalOpen(false);
          setCheckoutOrder(null);
        }}
        onPaymentSuccess={handlePaymentSuccess}
      />
    </div>
  );
};

export default App;
