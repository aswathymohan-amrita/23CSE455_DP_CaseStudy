package org.openwms.casestudy.ch03.exception;

public class ReorderRequestNotFoundException extends RuntimeException {

    public ReorderRequestNotFoundException(String requestId) {
        super("Unknown reorder request: " + requestId);
    }
}
