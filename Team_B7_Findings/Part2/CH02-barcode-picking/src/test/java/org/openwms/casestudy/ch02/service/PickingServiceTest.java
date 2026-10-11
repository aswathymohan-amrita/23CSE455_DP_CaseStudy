package org.openwms.casestudy.ch02.service;

import org.junit.jupiter.api.Test;
import org.openwms.casestudy.ch02.exception.InsufficientStockException;
import org.openwms.casestudy.ch02.exception.InvalidPickingQuantityException;
import org.openwms.casestudy.ch02.exception.StockUnavailableException;
import org.openwms.casestudy.ch02.domain.StockItem;
import org.openwms.casestudy.ch02.repository.InMemoryStockRepository;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class PickingServiceTest {

    @Test
    void picks_a_requested_quantity_by_stock_item_id() {
        var repository = new InMemoryStockRepository();
        var item = new StockItem("STOCK-TEST", "TEST-BARCODE", "TEST-PRODUCT", "B-01-01", 5, true);
        repository.save(item);

        var result = new PickingService(repository, new BarcodeResolver(repository)).pickByItemId("STOCK-TEST", 2);

        assertThat(result.quantityPicked()).isEqualTo(2);
        assertThat(result.remainingQuantity()).isEqualTo(3);
        assertThat(repository.findById("STOCK-TEST").orElseThrow().availableQuantity()).isEqualTo(3);
    }

    @Test
    void picks_stock_resolved_from_a_barcode_and_decreases_quantity() {
        var repository = repositoryWith(new StockItem("STOCK-TEST", "BAR-TEST", "PRODUCT-TEST", "B-01-01", 5, true));
        var service = new PickingService(repository, new BarcodeResolver(repository));

        var result = service.pickByBarcode("BAR-TEST", 2);

        assertThat(result.barcode()).isEqualTo("BAR-TEST");
        assertThat(result.itemId()).isEqualTo("STOCK-TEST");
        assertThat(result.productCode()).isEqualTo("PRODUCT-TEST");
        assertThat(result.quantityPicked()).isEqualTo(2);
        assertThat(result.location()).isEqualTo("B-01-01");
        assertThat(result.remainingQuantity()).isEqualTo(3);
        assertThat(repository.findById("STOCK-TEST").orElseThrow().availableQuantity()).isEqualTo(3);
    }

    @Test
    void rejects_quantity_greater_than_available_stock() {
        var repository = repositoryWith(new StockItem("STOCK-TEST", "BAR-TEST", "PRODUCT-TEST", "B-01-01", 2, true));
        var service = new PickingService(repository, new BarcodeResolver(repository));

        assertThatThrownBy(() -> service.pickByBarcode("BAR-TEST", 3))
                .isInstanceOf(InsufficientStockException.class);
    }

    @Test
    void rejects_zero_and_negative_quantities() {
        var item = new StockItem("STOCK-TEST", "BAR-TEST", "PRODUCT-TEST", "B-01-01", 5, true);
        var repository = repositoryWith(item);
        var service = new PickingService(repository, new BarcodeResolver(repository));

        assertThatThrownBy(() -> service.pickByBarcode("BAR-TEST", 0))
                .isInstanceOf(InvalidPickingQuantityException.class);
        assertThatThrownBy(() -> service.pickByBarcode("BAR-TEST", -1))
                .isInstanceOf(InvalidPickingQuantityException.class);
        assertThat(item.availableQuantity()).isEqualTo(5);
    }

    @Test
    void rejects_unavailable_stock() {
        var repository = repositoryWith(new StockItem("STOCK-OUT", "BAR-OUT", "PRODUCT-OUT", "C-01-01", 0, false));
        var service = new PickingService(repository, new BarcodeResolver(repository));

        assertThatThrownBy(() -> service.pickByBarcode("BAR-OUT", 1))
                .isInstanceOf(StockUnavailableException.class);
    }

    @Test
    void direct_item_id_picking_remains_available_separately() {
        var repository = repositoryWith(new StockItem("STOCK-TEST", "BAR-TEST", "PRODUCT-TEST", "B-01-01", 5, true));
        var result = new PickingService(repository, new BarcodeResolver(repository)).pickByItemId("STOCK-TEST", 1);

        assertThat(result.itemId()).isEqualTo("STOCK-TEST");
        assertThat(result.remainingQuantity()).isEqualTo(4);
    }

    private InMemoryStockRepository repositoryWith(StockItem item) {
        var repository = new InMemoryStockRepository();
        repository.save(item);
        return repository;
    }
}
