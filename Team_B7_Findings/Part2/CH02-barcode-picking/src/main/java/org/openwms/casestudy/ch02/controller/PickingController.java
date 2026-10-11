package org.openwms.casestudy.ch02.controller;

import org.openwms.casestudy.ch02.domain.PickingResult;
import org.openwms.casestudy.ch02.domain.PickingRequest;
import org.openwms.casestudy.ch02.service.PickingService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/picking")
public class PickingController {

    private final PickingService pickingService;

    public PickingController(PickingService pickingService) {
        this.pickingService = pickingService;
    }

    @PostMapping("/item")
    public PickingResult pickByItemId(@RequestBody ItemPickingRequest request) {
        return pickingService.pickByItemId(request.itemId(), request.quantity());
    }

    @PostMapping("/barcode")
    public PickingResult pickByBarcode(@Valid @RequestBody PickingRequest request) {
        return pickingService.pickByBarcode(request.barcode(), request.quantity());
    }

    public record ItemPickingRequest(String itemId, int quantity) {
    }
}
