package org.openwms.casestudy.ch03.domain;

import org.openwms.casestudy.ch03.exception.InsufficientStockException;
import org.openwms.casestudy.ch03.exception.InvalidStockQuantityException;

public class StockItem {

    private final String id;
    private int availableQuantity;

    public StockItem(String id, int availableQuantity) {
        if (availableQuantity < 0) {
            throw new IllegalArgumentException("Available quantity must not be negative");
        }
        this.id = id;
        this.availableQuantity = availableQuantity;
    }

    public String id() {
        return id;
    }

    public String getId() {
        return id;
    }

    public synchronized int availableQuantity() {
        return availableQuantity;
    }

    public synchronized int getAvailableQuantity() {
        return availableQuantity;
    }

    public synchronized void consume(int quantity) {
        if (quantity <= 0) {
            throw new InvalidStockQuantityException("Quantity must be greater than zero");
        }
        if (quantity > availableQuantity) {
            throw new InsufficientStockException("Cannot consume more than available stock");
        }
        availableQuantity -= quantity;
    }

    public synchronized void replenish(int quantity) {
        if (quantity <= 0) {
            throw new InvalidStockQuantityException("Quantity must be greater than zero");
        }
        availableQuantity = Math.addExact(availableQuantity, quantity);
    }
}
