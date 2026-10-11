package org.openwms.casestudy.ch02.domain;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

public record PickingRequest(
        @NotBlank String barcode,
        @Min(1) int quantity
) {
}
