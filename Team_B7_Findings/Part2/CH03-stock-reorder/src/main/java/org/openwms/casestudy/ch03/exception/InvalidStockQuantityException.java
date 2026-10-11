package org.openwms.casestudy.ch03.exception;

public class InvalidStockQuantityException extends RuntimeException {

    public InvalidStockQuantityException(String message) {
        super(message);
    }
}
