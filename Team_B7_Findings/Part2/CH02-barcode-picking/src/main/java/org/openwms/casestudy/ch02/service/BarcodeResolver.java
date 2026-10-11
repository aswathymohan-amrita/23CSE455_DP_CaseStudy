package org.openwms.casestudy.ch02.service;

import org.openwms.casestudy.ch02.domain.StockItem;
import org.openwms.casestudy.ch02.exception.BarcodeNotFoundException;
import org.openwms.casestudy.ch02.repository.StockRepository;
import org.springframework.stereotype.Component;

@Component
public class BarcodeResolver {

    private final StockRepository stockRepository;

    public BarcodeResolver(StockRepository stockRepository) {
        this.stockRepository = stockRepository;
    }

    public StockItem resolve(String barcode) {
        return stockRepository.findByBarcode(barcode)
                .orElseThrow(() -> new BarcodeNotFoundException(barcode));
    }
}
