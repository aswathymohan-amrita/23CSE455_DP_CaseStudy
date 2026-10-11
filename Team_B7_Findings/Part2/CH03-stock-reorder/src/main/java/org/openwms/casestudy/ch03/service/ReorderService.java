package org.openwms.casestudy.ch03.service;

import org.openwms.casestudy.ch03.domain.ReorderRequest;
import org.openwms.casestudy.ch03.domain.ReorderRule;
import org.openwms.casestudy.ch03.domain.ReorderStatus;
import org.openwms.casestudy.ch03.exception.InvalidReorderStatusException;
import org.openwms.casestudy.ch03.exception.ReorderRuleNotFoundException;
import org.openwms.casestudy.ch03.exception.ReorderRequestNotFoundException;
import org.openwms.casestudy.ch03.exception.StockNotFoundException;
import org.openwms.casestudy.ch03.repository.ReorderRequestRepository;
import org.openwms.casestudy.ch03.repository.ReorderRuleRepository;
import org.openwms.casestudy.ch03.repository.StockRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class ReorderService {

    private final StockRepository stockRepository;
    private final ReorderRuleRepository ruleRepository;
    private final ReorderRequestRepository requestRepository;
    private final AtomicLong requestSequence = new AtomicLong();

    public ReorderService(
            StockRepository stockRepository,
            ReorderRuleRepository ruleRepository,
            ReorderRequestRepository requestRepository
    ) {
        this.stockRepository = stockRepository;
        this.ruleRepository = ruleRepository;
        this.requestRepository = requestRepository;
    }

    public ReorderRule saveRule(ReorderRule rule) {
        if (stockRepository.findById(rule.itemId()).isEmpty()) {
            throw new StockNotFoundException(rule.itemId());
        }
        ruleRepository.save(rule);
        return rule;
    }

    public ReorderRule findRule(String itemId) {
        if (stockRepository.findById(itemId).isEmpty()) {
            throw new StockNotFoundException(itemId);
        }
        return ruleRepository.findByItemId(itemId)
                .orElseThrow(() -> new ReorderRuleNotFoundException(itemId));
    }

    public synchronized Optional<ReorderRequest> evaluate(String itemId) {
        var stockItem = stockRepository.findById(itemId)
                .orElseThrow(() -> new StockNotFoundException(itemId));
        var openRequest = requestRepository.findOpenByItemId(itemId);
        if (openRequest.isPresent()) {
            return openRequest;
        }
        var rule = ruleRepository.findByItemId(itemId);
        if (rule.isEmpty()) {
            return Optional.empty();
        }
        var available = stockItem.availableQuantity();
        var quantity = rule.get().reorderQuantity(available);
        if (quantity == 0) {
            return Optional.empty();
        }
        var request = new ReorderRequest(
                "REORDER-%06d".formatted(requestSequence.incrementAndGet()),
                itemId,
                quantity,
                available
        );
        requestRepository.save(request);
        return Optional.of(request);
    }

    public List<ReorderRequest> findAll() {
        return requestRepository.findAll();
    }

    public ReorderRequest findById(String requestId) {
        return requestRepository.findById(requestId)
                .orElseThrow(() -> new ReorderRequestNotFoundException(requestId));
    }

    public synchronized ReorderRequest complete(String requestId) {
        var request = findById(requestId);
        if (request.status() != ReorderStatus.OPEN) {
            throw new InvalidReorderStatusException(requestId);
        }
        var stockItem = stockRepository.findById(request.itemId())
                .orElseThrow(() -> new StockNotFoundException(request.itemId()));
        stockItem.replenish(request.quantity());
        stockRepository.save(stockItem);
        request.complete();
        requestRepository.save(request);
        return request;
    }
}
