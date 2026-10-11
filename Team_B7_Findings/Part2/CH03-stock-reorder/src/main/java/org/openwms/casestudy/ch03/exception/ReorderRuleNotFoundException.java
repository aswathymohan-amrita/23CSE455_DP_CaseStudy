package org.openwms.casestudy.ch03.exception;

public class ReorderRuleNotFoundException extends RuntimeException {

    public ReorderRuleNotFoundException(String itemId) {
        super("No reorder rule configured for stock item: " + itemId);
    }
}
