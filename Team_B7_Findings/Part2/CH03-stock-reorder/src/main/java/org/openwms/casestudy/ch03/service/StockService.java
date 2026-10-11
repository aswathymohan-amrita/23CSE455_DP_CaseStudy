package org.openwms.casestudy.ch03.service;

import org.openwms.casestudy.ch03.domain.StockItem;
import org.openwms.casestudy.ch03.exception.StockNotFoundException;
import org.openwms.casestudy.ch03.repository.StockRepository;
import org.springframework.stereotype.Service;

@Service
public class StockService {

    private final StockRepository stockRepository;
    private final ReorderService reorderService;

    public StockService(StockRepository stockRepository, ReorderService reorderService) {
        this.stockRepository = stockRepository;
        this.reorderService = reorderService;
    }

    public StockItem find(String itemId) {
        return stockRepository.findById(itemId)
                .orElseThrow(() -> new StockNotFoundException(itemId));
    }

    public synchronized StockItem consume(String itemId, int quantity) {
        var stockItem = find(itemId);
        stockItem.consume(quantity);
        stockRepository.save(stockItem);
        reorderService.evaluate(itemId);
        return stockItem;
    }
}
