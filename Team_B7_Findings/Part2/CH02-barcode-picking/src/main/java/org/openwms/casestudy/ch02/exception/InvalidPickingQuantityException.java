package org.openwms.casestudy.ch02.exception;

public class InvalidPickingQuantityException extends RuntimeException {

    public InvalidPickingQuantityException(String message) {
        super(message);
    }
}
