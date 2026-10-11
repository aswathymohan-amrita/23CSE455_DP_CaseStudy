package org.openwms.casestudy.ch03.exception;

public class InvalidReorderRuleException extends RuntimeException {

    public InvalidReorderRuleException(String message) {
        super(message);
    }
}
