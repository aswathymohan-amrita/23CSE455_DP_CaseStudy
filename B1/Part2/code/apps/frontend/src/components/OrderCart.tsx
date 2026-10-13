import React from 'react';
import { Order } from '../types/order.types';

interface OrderCartProps {
  order: Order | null;
  onRemoveItem: (itemId: string) => void;
  onUpdateQuantity: (itemId: string, quantity: number) => void;
  onSubmitOrder: () => void;
  onCancelOrder: () => void;
}

export const OrderCart: React.FC<OrderCartProps> = ({
  order,
  onRemoveItem,
  onUpdateQuantity,
  onSubmitOrder,
  onCancelOrder,
}) => {
  if (!order) {
    return (
      <div className="order-cart empty">
        <p>No active order</p>
      </div>
    );
  }

  const subtotal = order.items.reduce((sum, item) => {
    return sum + (item.menuItem.price * item.quantity);
  }, 0);

  const tax = subtotal * 0.08;
  const total = subtotal + tax;

  return (
    <div className="order-cart">
      <div className="cart-header">
        <h3>Order #{order.id.slice(0, 8)}</h3>
        <span className={`status ${order.status.toLowerCase()}`}>
          {order.status}
        </span>
      </div>

      <div className="cart-items">
        {order.items.length === 0 ? (
          <p className="empty-message">No items in order</p>
        ) : (
          order.items.map((item) => (
            <div key={item.id} className="cart-item">
              <div className="item-info">
                <div className="item-name">{item.menuItem.name}</div>
                {item.notes && (
                  <div className="item-notes">{item.notes}</div>
                )}
                <div className="item-price">
                  ${item.menuItem.price.toFixed(2)}
                </div>
              </div>
              
              <div className="item-controls">
                <button
                  onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}
                  disabled={item.quantity <= 1}
                  className="btn-quantity"
                >
                  -
                </button>
                <span className="quantity">{item.quantity}</span>
                <button
                  onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
                  className="btn-quantity"
                >
                  +
                </button>
                <button
                  onClick={() => onRemoveItem(item.id)}
                  className="btn-remove"
                >
                  ×
                </button>
              </div>

              <div className="item-total">
                ${(item.menuItem.price * item.quantity).toFixed(2)}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="cart-summary">
        <div className="summary-row">
          <span>Subtotal</span>
          <span>${subtotal.toFixed(2)}</span>
        </div>
        <div className="summary-row">
          <span>Tax (8%)</span>
          <span>${tax.toFixed(2)}</span>
        </div>
        <div className="summary-row total">
          <span>Total</span>
          <span>${total.toFixed(2)}</span>
        </div>
      </div>

      <div className="cart-actions">
        <button onClick={onCancelOrder} className="btn-cancel">
          Cancel Order
        </button>
        <button
          onClick={onSubmitOrder}
          className="btn-submit"
          disabled={order.items.length === 0}
        >
          Submit Order
        </button>
      </div>
    </div>
  );
};

export default OrderCart;
