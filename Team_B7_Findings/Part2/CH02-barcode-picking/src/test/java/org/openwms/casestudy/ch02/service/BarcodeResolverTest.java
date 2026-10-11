package org.openwms.casestudy.ch02.service;

import org.junit.jupiter.api.Test;
import org.openwms.casestudy.ch02.domain.StockItem;
import org.openwms.casestudy.ch02.exception.BarcodeNotFoundException;
import org.openwms.casestudy.ch02.repository.InMemoryStockRepository;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class BarcodeResolverTest {

    private final InMemoryStockRepository repository = new InMemoryStockRepository();
    private final BarcodeResolver resolver = new BarcodeResolver(repository);

    @Test
    void resolves_an_existing_barcode_to_its_stock_item() {
        var stockItem = new StockItem("STOCK-TEST", "BAR-TEST", "PRODUCT-TEST", "B-01-01", 4, true);
        repository.save(stockItem);

        assertThat(resolver.resolve("BAR-TEST")).isSameAs(stockItem);
    }

    @Test
    void rejects_an_unknown_barcode_without_creating_stock() {
        assertThatThrownBy(() -> resolver.resolve("UNKNOWN"))
                .isInstanceOf(BarcodeNotFoundException.class)
                .hasMessageContaining("UNKNOWN");
        assertThat(repository.findByBarcode("UNKNOWN")).isEmpty();
    }
}
