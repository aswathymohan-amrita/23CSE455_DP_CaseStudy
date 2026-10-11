package org.openwms.casestudy.ch02.domain;

import org.openwms.casestudy.ch02.exception.InsufficientStockException;
import org.openwms.casestudy.ch02.exception.InvalidPickingQuantityException;
import org.openwms.casestudy.ch02.exception.StockUnavailableException;

public class StockItem {

    private final String id;
    private final String barcode;
    private final String productCode;
    private final String location;
    private int availableQuantity;
    private boolean available;

    public StockItem(String id, String barcode, String productCode, String location, int availableQuantity, boolean available) {
        this.id = id;
        this.barcode = barcode;
        this.productCode = productCode;
        this.location = location;
        this.availableQuantity = availableQuantity;
        this.available = available;
    }

    public String id() {
        return id;
    }

    public String barcode() {
        return barcode;
    }

    public String productCode() {
        return productCode;
    }

    public String location() {
        return location;
    }

    public int availableQuantity() {
        return availableQuantity;
    }

    public boolean isAvailable() {
        return available;
    }

    public synchronized void pick(int quantity) {
        if (quantity <= 0) {
            throw new InvalidPickingQuantityException("Quantity must be greater than zero");
        }
        if (!available || availableQuantity == 0) {
            throw new StockUnavailableException("Stock item is unavailable");
        }
        if (quantity > availableQuantity) {
            throw new InsufficientStockException("Requested quantity exceeds available stock");
        }
        availableQuantity -= quantity;
        if (availableQuantity == 0) {
            available = false;
        }
    }
}
