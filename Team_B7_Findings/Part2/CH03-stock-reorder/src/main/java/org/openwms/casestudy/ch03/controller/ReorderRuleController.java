package org.openwms.casestudy.ch03.controller;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import org.openwms.casestudy.ch03.domain.ReorderRule;
import org.openwms.casestudy.ch03.service.ReorderService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/reorder-rules")
public class ReorderRuleController {

    private final ReorderService reorderService;

    public ReorderRuleController(ReorderService reorderService) {
        this.reorderService = reorderService;
    }

    @PutMapping("/{itemId}")
    public ReorderRule putRule(@PathVariable String itemId, @Valid @RequestBody ReorderRuleRequest request) {
        return reorderService.saveRule(new ReorderRule(itemId, request.reorderThreshold(), request.targetQuantity()));
    }

    @GetMapping("/{itemId}")
    public ReorderRule getRule(@PathVariable String itemId) {
        return reorderService.findRule(itemId);
    }

    public record ReorderRuleRequest(
            @Min(0) int reorderThreshold,
            @Min(1) int targetQuantity
    ) {
    }
}
