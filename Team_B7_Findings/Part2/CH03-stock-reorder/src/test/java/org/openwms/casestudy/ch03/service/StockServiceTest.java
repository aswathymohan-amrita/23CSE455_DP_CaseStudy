package org.openwms.casestudy.ch03.service;

import org.junit.jupiter.api.Test;
import org.openwms.casestudy.ch03.exception.StockNotFoundException;
import org.openwms.casestudy.ch03.repository.InMemoryReorderRequestRepository;
import org.openwms.casestudy.ch03.repository.InMemoryReorderRuleRepository;
import org.openwms.casestudy.ch03.repository.InMemoryStockRepository;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class StockServiceTest {

    @Test
    void consumption_reduces_stock_without_creating_a_reorder() {
        var stockRepository = new InMemoryStockRepository();
        var service = new StockService(stockRepository, new ReorderService(
                stockRepository,
                new InMemoryReorderRuleRepository(),
                new InMemoryReorderRequestRepository()));

        var updated = service.consume("ITEM-001", 7);

        assertThat(updated.availableQuantity()).isEqualTo(3);
    }

    @Test
    void unknown_item_is_rejected() {
        var stockRepository = new InMemoryStockRepository();
        var service = new StockService(stockRepository, new ReorderService(
                stockRepository,
                new InMemoryReorderRuleRepository(),
                new InMemoryReorderRequestRepository()));

        assertThatThrownBy(() -> service.consume("MISSING", 1))
                .isInstanceOf(StockNotFoundException.class)
                .hasMessageContaining("Unknown stock item");
    }
}
