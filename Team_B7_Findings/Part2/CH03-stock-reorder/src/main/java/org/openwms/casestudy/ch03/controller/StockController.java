package org.openwms.casestudy.ch03.controller;

import org.openwms.casestudy.ch03.domain.StockItem;
import org.openwms.casestudy.ch03.service.StockService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/stock")
public class StockController {

    private final StockService stockService;

    public StockController(StockService stockService) {
        this.stockService = stockService;
    }

    @GetMapping("/{itemId}")
    public StockItem get(@PathVariable String itemId) {
        return stockService.find(itemId);
    }

    @PostMapping("/{itemId}/consume")
    public StockItem consume(@PathVariable String itemId, @Valid @RequestBody ConsumeRequest request) {
        return stockService.consume(itemId, request.quantity());
    }

    public record ConsumeRequest(@Min(1) int quantity) {
    }
}
