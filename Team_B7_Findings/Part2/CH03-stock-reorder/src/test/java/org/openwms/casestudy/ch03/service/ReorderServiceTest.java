package org.openwms.casestudy.ch03.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openwms.casestudy.ch03.domain.ReorderRule;
import org.openwms.casestudy.ch03.domain.ReorderStatus;
import org.openwms.casestudy.ch03.exception.StockNotFoundException;
import org.openwms.casestudy.ch03.repository.InMemoryReorderRequestRepository;
import org.openwms.casestudy.ch03.repository.InMemoryReorderRuleRepository;
import org.openwms.casestudy.ch03.repository.InMemoryStockRepository;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class ReorderServiceTest {

    private InMemoryStockRepository stockRepository;
    private InMemoryReorderRuleRepository ruleRepository;
    private InMemoryReorderRequestRepository requestRepository;
    private ReorderService reorderService;
    private StockService stockService;

    @BeforeEach
    void setUp() {
        stockRepository = new InMemoryStockRepository();
        ruleRepository = new InMemoryReorderRuleRepository();
        requestRepository = new InMemoryReorderRequestRepository();
        reorderService = new ReorderService(stockRepository, ruleRepository, requestRepository);
        stockService = new StockService(stockRepository, reorderService);
    }

    @Test
    void repeated_evaluation_reuses_the_open_request() {
        reorderService.saveRule(new ReorderRule("ITEM-002", 5, 10));

        var first = reorderService.evaluate("ITEM-002").orElseThrow();
        var second = reorderService.evaluate("ITEM-002").orElseThrow();

        assertThat(second).isSameAs(first);
        assertThat(reorderService.findAll()).containsExactly(first);
    }

    @Test
    void stock_above_threshold_does_not_create_a_request() {
        rule(5, 10);

        assertThat(reorderService.evaluate("ITEM-001")).isEmpty();
        assertThat(reorderService.findAll()).isEmpty();
    }

    @Test
    void stock_equal_to_threshold_creates_a_request_for_the_gap_to_target() {
        rule(5, 10);
        stockService.consume("ITEM-001", 5);

        var request = reorderService.evaluate("ITEM-001").orElseThrow();

        assertThat(request.availableQuantityAtTrigger()).isEqualTo(5);
        assertThat(request.quantity()).isEqualTo(5);
    }

    @Test
    void stock_below_threshold_creates_a_request_for_the_gap_to_target() {
        reorderService.saveRule(new ReorderRule("ITEM-002", 5, 10));

        var request = reorderService.evaluate("ITEM-002").orElseThrow();

        assertThat(request.availableQuantityAtTrigger()).isEqualTo(3);
        assertThat(request.quantity()).isEqualTo(7);
    }

    @Test
    void automatic_reorder_after_consumption_and_completion_allow_a_future_request() {
        rule(5, 10);
        stockService.consume("ITEM-001", 5);
        var first = requestRepository.findAll().get(0);
        assertThat(first.quantity()).isEqualTo(5);
        assertThat(first.status()).isEqualTo(ReorderStatus.OPEN);

        var completed = reorderService.complete(first.id());
        assertThat(completed.status()).isEqualTo(ReorderStatus.COMPLETED);
        assertThat(stockService.find("ITEM-001").availableQuantity()).isEqualTo(10);

        stockService.consume("ITEM-001", 6);
        var requests = reorderService.findAll();
        assertThat(requests).hasSize(2);
        assertThat(requests.get(1).id()).isNotEqualTo(first.id());
        assertThat(requests.get(1).quantity()).isEqualTo(6);
        assertThat(requests.get(1).status()).isEqualTo(ReorderStatus.OPEN);
    }

    @Test
    void unknown_stock_item_is_rejected_when_evaluating() {
        assertThatThrownBy(() -> reorderService.evaluate("MISSING"))
                .isInstanceOf(StockNotFoundException.class);
    }

    @Test
    void reorder_request_can_be_retrieved_by_id_and_as_a_list() {
        rule(5, 10);
        stockService.consume("ITEM-001", 7);
        var created = requestRepository.findAll().get(0);

        assertThat(reorderService.findById(created.id())).isSameAs(created);
        assertThat(reorderService.findAll()).containsExactly(created);
    }

    @Test
    void completing_an_already_completed_request_is_rejected() {
        rule(5, 10);
        stockService.consume("ITEM-001", 5);
        var created = requestRepository.findAll().get(0);
        reorderService.complete(created.id());

        assertThatThrownBy(() -> reorderService.complete(created.id()))
                .isInstanceOf(org.openwms.casestudy.ch03.exception.InvalidReorderStatusException.class);
    }

    private void rule(int threshold, int target) {
        reorderService.saveRule(new ReorderRule("ITEM-001", threshold, target));
    }
}
