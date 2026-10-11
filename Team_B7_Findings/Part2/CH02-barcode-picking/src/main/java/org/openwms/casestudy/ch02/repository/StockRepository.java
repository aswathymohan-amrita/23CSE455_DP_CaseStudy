package org.openwms.casestudy.ch02.repository;

import org.openwms.casestudy.ch02.domain.StockItem;

import java.util.Optional;

public interface StockRepository {

    Optional<StockItem> findById(String id);

    Optional<StockItem> findByBarcode(String barcode);

    void save(StockItem stockItem);
}
