package org.openwms.casestudy.ch02.service;

import org.openwms.casestudy.ch02.domain.PickingResult;
import org.openwms.casestudy.ch02.domain.StockItem;
import org.openwms.casestudy.ch02.repository.StockRepository;
import org.springframework.stereotype.Service;

@Service
public class PickingService {

    private final StockRepository stockRepository;
    private final BarcodeResolver barcodeResolver;

    public PickingService(StockRepository stockRepository, BarcodeResolver barcodeResolver) {
        this.stockRepository = stockRepository;
        this.barcodeResolver = barcodeResolver;
    }

    public PickingResult pickByItemId(String itemId, int quantity) {
        var stockItem = stockRepository.findById(itemId)
                .orElseThrow(() -> new IllegalArgumentException("Unknown stock item: " + itemId));
        return pick(stockItem, quantity);
    }

    public PickingResult pickByBarcode(String barcode, int quantity) {
        return pick(barcodeResolver.resolve(barcode), quantity);
    }

    private PickingResult pick(StockItem stockItem, int quantity) {
        stockItem.pick(quantity);
        stockRepository.save(stockItem);
        return new PickingResult(stockItem.id(), stockItem.barcode(), stockItem.productCode(), quantity, stockItem.location(),
                stockItem.availableQuantity());
    }
}
