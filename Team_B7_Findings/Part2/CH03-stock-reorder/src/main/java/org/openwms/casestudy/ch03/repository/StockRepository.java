package org.openwms.casestudy.ch03.repository;

import org.openwms.casestudy.ch03.domain.StockItem;

import java.util.Optional;

public interface StockRepository {

    Optional<StockItem> findById(String itemId);

    void save(StockItem stockItem);
}
