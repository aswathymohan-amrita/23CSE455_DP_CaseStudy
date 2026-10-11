package org.openwms.casestudy.ch03.exception;

public class InvalidReorderStatusException extends RuntimeException {

    public InvalidReorderStatusException(String requestId) {
        super("Reorder request is already completed: " + requestId);
    }
}
