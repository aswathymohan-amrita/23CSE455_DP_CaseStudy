package org.openwms.casestudy.ch02.repository;

import org.openwms.casestudy.ch02.domain.StockItem;
import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class InMemoryStockRepository implements StockRepository {

    private final Map<String, StockItem> items = new ConcurrentHashMap<>();

    public InMemoryStockRepository() {
        save(new StockItem("STOCK-001", "8901234567890", "ITEM-001", "A-01-01", 10, true));
    }

    @Override
    public Optional<StockItem> findById(String id) {
        return Optional.ofNullable(items.get(id));
    }

    @Override
    public Optional<StockItem> findByBarcode(String barcode) {
        return items.values().stream()
                .filter(item -> item.barcode().equals(barcode))
                .findFirst();
    }

    @Override
    public void save(StockItem stockItem) {
        items.put(stockItem.id(), stockItem);
    }
}
