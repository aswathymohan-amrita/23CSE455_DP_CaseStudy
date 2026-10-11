package org.openwms.casestudy.ch03.repository;

import org.openwms.casestudy.ch03.domain.StockItem;
import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class InMemoryStockRepository implements StockRepository {

    private final Map<String, StockItem> items = new ConcurrentHashMap<>();

    public InMemoryStockRepository() {
        save(new StockItem("ITEM-001", 10));
        save(new StockItem("ITEM-002", 3));
    }

    @Override
    public Optional<StockItem> findById(String itemId) {
        return Optional.ofNullable(items.get(itemId));
    }

    @Override
    public void save(StockItem stockItem) {
        items.put(stockItem.id(), stockItem);
    }
}
