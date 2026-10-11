package org.openwms.casestudy.ch03.controller;

import org.openwms.casestudy.ch03.domain.ReorderRequest;
import org.openwms.casestudy.ch03.service.ReorderService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/reorders")
public class ReorderController {

    private final ReorderService reorderService;

    public ReorderController(ReorderService reorderService) {
        this.reorderService = reorderService;
    }

    @GetMapping
    public List<ReorderRequest> getAll() {
        return reorderService.findAll();
    }

    @GetMapping("/{requestId}")
    public ReorderRequest getById(@PathVariable String requestId) {
        return reorderService.findById(requestId);
    }

    @PostMapping("/evaluate/{itemId}")
    public ResponseEntity<ReorderRequest> evaluate(@PathVariable String itemId) {
        return reorderService.evaluate(itemId)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.noContent().build());
    }

    @PostMapping("/{requestId}/complete")
    public ResponseEntity<ReorderRequest> complete(@PathVariable String requestId) {
        return ResponseEntity.ok(reorderService.complete(requestId));
    }
}
