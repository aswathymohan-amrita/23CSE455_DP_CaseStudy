package org.openwms.casestudy.ch02.domain;

public record PickingResult(
        String itemId,
        String barcode,
        String productCode,
        int quantityPicked,
        String location,
        int remainingQuantity
) {
}
