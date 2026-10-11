package org.openwms.casestudy.ch03.domain;

public class ReorderRequest {

    private final String id;
    private final String itemId;
    private final int quantity;
    private final int availableQuantityAtTrigger;
    private ReorderStatus status;

    public ReorderRequest(String id, String itemId, int quantity, int availableQuantityAtTrigger) {
        this.id = id;
        this.itemId = itemId;
        this.quantity = quantity;
        this.availableQuantityAtTrigger = availableQuantityAtTrigger;
        this.status = ReorderStatus.OPEN;
    }

    public String id() {
        return id;
    }

    public String getId() {
        return id;
    }

    public String itemId() {
        return itemId;
    }

    public String getItemId() {
        return itemId;
    }

    public int quantity() {
        return quantity;
    }

    public int getQuantity() {
        return quantity;
    }

    public int availableQuantityAtTrigger() {
        return availableQuantityAtTrigger;
    }

    public int getAvailableQuantityAtTrigger() {
        return availableQuantityAtTrigger;
    }

    public synchronized ReorderStatus status() {
        return status;
    }

    public synchronized ReorderStatus getStatus() {
        return status;
    }

    public synchronized void complete() {
        status = ReorderStatus.COMPLETED;
    }
}
