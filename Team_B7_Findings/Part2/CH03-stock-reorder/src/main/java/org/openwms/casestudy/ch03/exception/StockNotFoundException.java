package org.openwms.casestudy.ch03.exception;

public class StockNotFoundException extends RuntimeException {

    public StockNotFoundException(String itemId) {
        super("Unknown stock item: " + itemId);
    }
}
