package org.openwms.casestudy.ch03.domain;

import org.openwms.casestudy.ch03.exception.InvalidReorderRuleException;

public record ReorderRule(String itemId, int reorderThreshold, int targetQuantity) {

    public ReorderRule {
        if (itemId == null || itemId.isBlank()) {
            throw new InvalidReorderRuleException("Item ID must not be blank");
        }
        if (reorderThreshold < 0) {
            throw new InvalidReorderRuleException("Reorder threshold must not be negative");
        }
        if (targetQuantity <= reorderThreshold) {
            throw new InvalidReorderRuleException("Target quantity must be greater than reorder threshold");
        }
    }

    public boolean requiresReorder(int availableQuantity) {
        return availableQuantity <= reorderThreshold && availableQuantity < targetQuantity;
    }

    public int reorderQuantity(int availableQuantity) {
        if (!requiresReorder(availableQuantity)) {
            return 0;
        }
        return targetQuantity - availableQuantity;
    }
}
