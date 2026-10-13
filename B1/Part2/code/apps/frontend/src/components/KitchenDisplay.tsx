import React, { useEffect, useState } from 'react';
import { Order, OrderItem, OrderItemStatus, OrderStatus } from '../types/order.types';
import { socketClient } from '../lib/socket';

interface KitchenDisplayProps {
  orders?: Order[];
  onItemStatusChange?: (orderId: string, itemId: string, newStatus: OrderItemStatus) => void;
}

export const KitchenDisplay: React.FC<KitchenDisplayProps> = ({
  orders: propOrders,
  onItemStatusChange: propOnItemStatusChange,
}) => {
  const [localOrders, setLocalOrders] = useState<Order[]>([]);
  const [statusFilter, setStatusFilter] = useState<'all' | 'pending' | 'preparing' | 'ready'>('all');
  const [stationFilter, setStationFilter] = useState<'all' | 'cold' | 'hot' | 'bar'>('all');

  // Use props if provided, otherwise fallback to local socket-fed orders
  const orders = propOrders !== undefined ? propOrders : localOrders;

  useEffect(() => {
    // Only connect socket if we're not exclusively using props
    const socket = socketClient.getSocket();
    if (!socket) return;

    // Join general kitchen and station-specific room
    socket.emit('kitchen:station:join', { station: stationFilter });

    // Handle full order broadcast
    socket.on('kitchen:order:new', (order: Order) => {
      setLocalOrders((prev) => {
        if (prev.some((o) => o.id === order.id)) return prev;
        return [order, ...prev];
      });
    });

    // Evolution 2: Handle station-targeted item arrivals
    socket.on('kitchen:station:item:new', (data: { orderId: string; orderNumber?: number; item: any; station: string }) => {
      setLocalOrders((prev) => {
        const existingOrder = prev.find((o) => o.id === data.orderId);
        if (existingOrder) {
          // Prevent duplicate items
          if (existingOrder.items.some((i) => i.id === data.item.id)) return prev;
          return prev.map((o) =>
            o.id === data.orderId ? { ...o, items: [...o.items, data.item] } : o
          );
        }
        // If order not present yet, construct container order
        const newOrder: Order = {
          id: data.orderId,
          tableId: 'kitchen-station',
          table: { id: 'station', number: `#${data.orderNumber || data.orderId.slice(-4)}` },
          status: OrderStatus.IN_PROGRESS,
          createdAt: new Date(),
          updatedAt: new Date(),
          items: [data.item],
        };
        return [newOrder, ...prev];
      });
    });

    socket.on('kitchen:order:updated', (updatedOrder: Order) => {
      setLocalOrders((prev) =>
        prev.map((order) => (order.id === updatedOrder.id ? updatedOrder : order))
      );
    });

    socket.on('kitchen:item:status:changed', ({ orderId, itemId, status }: any) => {
      setLocalOrders((prev) =>
        prev.map((order) => {
          if (order.id === orderId) {
            return {
              ...order,
              items: order.items.map((item) =>
                item.id === itemId ? { ...item, status: status as OrderItemStatus } : item
              ),
            };
          }
          return order;
        })
      );
    });

    socket.on('kitchen:item:completed', ({ orderId, itemId }: any) => {
      setLocalOrders((prev) =>
        prev.map((order) => {
          if (order.id === orderId) {
            return {
              ...order,
              items: order.items.map((item) =>
                item.id === itemId ? { ...item, status: OrderItemStatus.READY } : item
              ),
            };
          }
          return order;
        })
      );
    });

    return () => {
      socket.off('kitchen:order:new');
      socket.off('kitchen:station:item:new');
      socket.off('kitchen:order:updated');
      socket.off('kitchen:item:status:changed');
      socket.off('kitchen:item:completed');
    };
  }, [stationFilter]);

  // Evolution 2: Explicit CourseType & Station metadata routing
  const getItemStation = (item: OrderItem): 'cold' | 'hot' | 'bar' => {
    // 1. Explicit course enum if available
    const course = (item as any).course?.toUpperCase();
    if (course === 'SALAD' || course === 'APPETIZER' || course === 'SOUP') return 'cold';
    if (course === 'BEVERAGE' || course === 'DESSERT') return 'bar';
    if (course === 'ENTREE' || course === 'SIDE') return 'hot';

    // 2. Fallback to category / name inspection
    const name = item.menuItem?.name?.toLowerCase() || '';
    if (name.includes('salad') || name.includes('calamari') || name.includes('bread') || name.includes('soup') || name.includes('starter')) {
      return 'cold';
    }
    if (name.includes('cocktail') || name.includes('lemonade') || name.includes('wine') || name.includes('cake') || name.includes('dessert') || name.includes('mousse') || name.includes('drink')) {
      return 'bar';
    }
    return 'hot';
  };

  const handleStatusChange = (orderId: string, itemId: string, newStatus: OrderItemStatus) => {
    if (propOnItemStatusChange) {
      propOnItemStatusChange(orderId, itemId, newStatus);
    } else {
      setLocalOrders((prev) =>
        prev.map((order) => {
          if (order.id === orderId) {
            return {
              ...order,
              items: order.items.map((item) =>
                item.id === itemId ? { ...item, status: newStatus } : item
              ),
            };
          }
          return order;
        })
      );
      try {
        const socket = socketClient.getSocket();
        socket?.emit('kitchen:station:item:status', { orderId, itemId, status: newStatus, station: stationFilter });
        socket?.emit('kitchen:item:complete', { orderId, itemId, status: newStatus });
      } catch (err) {
        console.error(err);
      }
    }
  };

  // Filter items per station & status
  const filterItems = (items: OrderItem[]) => {
    return items.filter((item) => {
      // Status filter
      if (statusFilter === 'pending' && item.status !== OrderItemStatus.PENDING) return false;
      if (statusFilter === 'preparing' && item.status !== OrderItemStatus.PREPARING) return false;
      if (statusFilter === 'ready' && item.status !== OrderItemStatus.READY) return false;

      // Station filter
      if (stationFilter !== 'all') {
        const station = getItemStation(item);
        if (station !== stationFilter) return false;
      }
      return true;
    });
  };

  // Only display orders that have active (non-cancelled / non-served) items
  const activeOrders = orders.filter((order) => {
    const relevantItems = filterItems(order.items);
    return relevantItems.length > 0;
  });

  return (
    <div className="kitchen-display">
      {/* KDS Header with Station Routing & Status Filters */}
      <div className="kds-header">
        <div>
          <h2>Kitchen Display System (KDS)</h2>
          <p style={{ color: '#78716c', fontSize: '0.875rem' }}>
            Evolution 2: Multi-Station Routing & Live Ticket Execution
          </p>
        </div>

        {/* Station Routing Tabs (Evolution 2) */}
        <div className="station-tabs">
          <button
            onClick={() => setStationFilter('all')}
            className={`station-btn ${stationFilter === 'all' ? 'active' : ''}`}
          >
            🏢 All Stations
          </button>
          <button
            onClick={() => setStationFilter('cold')}
            className={`station-btn ${stationFilter === 'cold' ? 'active' : ''}`}
          >
            🧊 Cold Station (Salads/Apps)
          </button>
          <button
            onClick={() => setStationFilter('hot')}
            className={`station-btn ${stationFilter === 'hot' ? 'active' : ''}`}
          >
            🔥 Hot Station (Mains/Grill)
          </button>
          <button
            onClick={() => setStationFilter('bar')}
            className={`station-btn ${stationFilter === 'bar' ? 'active' : ''}`}
          >
            🍹 Bar & Desserts
          </button>
        </div>

        {/* Status Filters */}
        <div className="filter-buttons">
          <button
            onClick={() => setStatusFilter('all')}
            className={statusFilter === 'all' ? 'active' : ''}
          >
            All Status
          </button>
          <button
            onClick={() => setStatusFilter('pending')}
            className={statusFilter === 'pending' ? 'active' : ''}
          >
            ⏳ Pending
          </button>
          <button
            onClick={() => setStatusFilter('preparing')}
            className={statusFilter === 'preparing' ? 'active' : ''}
          >
            👨‍🍳 Cooking
          </button>
          <button
            onClick={() => setStatusFilter('ready')}
            className={statusFilter === 'ready' ? 'active' : ''}
          >
            ✅ Ready
          </button>
        </div>
      </div>

      {/* Orders Grid */}
      <div className="orders-grid">
        {activeOrders.length === 0 ? (
          <div className="no-orders" style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '3rem' }}>
            <span style={{ fontSize: '3rem', display: 'block', marginBottom: '0.5rem' }}>🍳</span>
            <h3 style={{ color: '#44403c' }}>No active tickets for selected filters</h3>
            <p style={{ color: '#78716c', marginTop: '0.25rem' }}>
              Place an order from the POS Terminal or Customer Online Ordering view to dispatch kitchen tickets!
            </p>
          </div>
        ) : (
          activeOrders.map((order) => {
            const filteredItems = filterItems(order.items);
            if (filteredItems.length === 0) return null;

            return (
              <div key={order.id} className="kds-ticket-card">
                <div className="ticket-header">
                  <div>
                    <span className="ticket-badge">
                      {order.table ? `Table #${order.table.number}` : '🛵 Online Order'}
                    </span>
                    <h3 className="ticket-id">Order #{order.id.slice(-6)}</h3>
                  </div>
                  <span className="ticket-time">
                    ⏱️ {new Date(order.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>

                <div className="ticket-items">
                  {filteredItems.map((item) => {
                    const station = getItemStation(item);
                    return (
                      <div key={item.id} className={`ticket-item ${item.status.toLowerCase()}`}>
                        <div className="ticket-item-left">
                          <span className="ticket-qty">{item.quantity}x</span>
                          <div>
                            <span className="ticket-name">{item.menuItem.name}</span>
                            <div className="ticket-station-pill">
                              {station === 'cold' ? '🧊 Cold' : station === 'bar' ? '🍹 Bar' : '🔥 Hot'}
                            </div>
                            {item.notes && <p className="ticket-note">Note: {item.notes}</p>}
                          </div>
                        </div>

                        <div className="ticket-actions">
                          {item.status === OrderItemStatus.PENDING && (
                            <button
                              onClick={() => handleStatusChange(order.id, item.id, OrderItemStatus.PREPARING)}
                              className="btn-cook"
                            >
                              ▶ Start Cooking
                            </button>
                          )}
                          {item.status === OrderItemStatus.PREPARING && (
                            <button
                              onClick={() => handleStatusChange(order.id, item.id, OrderItemStatus.READY)}
                              className="btn-ready"
                            >
                              ✓ Mark Ready
                            </button>
                          )}
                          {item.status === OrderItemStatus.READY && (
                            <button
                              onClick={() => handleStatusChange(order.id, item.id, OrderItemStatus.SERVED)}
                              className="btn-served"
                            >
                              🍽️ Mark Served
                            </button>
                          )}
                          {item.status === OrderItemStatus.SERVED && (
                            <span className="badge-served">Served ✓</span>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default KitchenDisplay;
