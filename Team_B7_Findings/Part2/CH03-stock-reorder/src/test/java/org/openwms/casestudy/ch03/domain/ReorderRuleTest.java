package org.openwms.casestudy.ch03.domain;

import org.junit.jupiter.api.Test;
import org.openwms.casestudy.ch03.exception.InvalidReorderRuleException;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class ReorderRuleTest {

    @Test
    void stock_above_threshold_does_not_require_reorder() {
        var rule = new ReorderRule("ITEM-001", 5, 10);

        assertThat(rule.requiresReorder(6)).isFalse();
        assertThat(rule.reorderQuantity(6)).isZero();
    }

    @Test
    void stock_equal_to_threshold_requires_reorder_to_target() {
        var rule = new ReorderRule("ITEM-001", 5, 10);

        assertThat(rule.requiresReorder(5)).isTrue();
        assertThat(rule.reorderQuantity(5)).isEqualTo(5);
    }

    @Test
    void stock_below_threshold_calculates_quantity_to_target() {
        var rule = new ReorderRule("ITEM-001", 5, 10);

        assertThat(rule.requiresReorder(3)).isTrue();
        assertThat(rule.reorderQuantity(3)).isEqualTo(7);
    }

    @Test
    void rejects_negative_threshold() {
        assertThatThrownBy(() -> new ReorderRule("ITEM-001", -1, 10))
                .isInstanceOf(InvalidReorderRuleException.class);
    }

    @Test
    void rejects_target_that_is_not_greater_than_threshold() {
        assertThatThrownBy(() -> new ReorderRule("ITEM-001", 5, 5))
                .isInstanceOf(InvalidReorderRuleException.class);
        assertThatThrownBy(() -> new ReorderRule("ITEM-001", 5, 4))
                .isInstanceOf(InvalidReorderRuleException.class);
    }
}
