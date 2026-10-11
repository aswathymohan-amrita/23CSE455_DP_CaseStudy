package org.openwms.casestudy.ch03.controller;

import org.junit.jupiter.api.Test;
import org.openwms.casestudy.ch03.domain.StockItem;
import org.openwms.casestudy.ch03.repository.InMemoryStockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.concurrent.atomic.AtomicLong;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class StockReorderControllerTest {

    private static final AtomicLong ITEM_SEQUENCE = new AtomicLong();

    @Autowired
    private MockMvc mockMvc;
    @Autowired
    private InMemoryStockRepository stockRepository;

    @Test
    void consuming_stock_automatically_creates_a_reorder_that_can_be_listed() throws Exception {
        var itemId = createStock(10);
        putRule(itemId, 5, 10);

        mockMvc.perform(post("/api/stock/{itemId}/consume", itemId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"quantity":7}
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.availableQuantity").value(3));

        mockMvc.perform(get("/api/reorders"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[?(@.itemId == '%s')].quantity".formatted(itemId)).value(org.hamcrest.Matchers.contains(7)));
    }

    @Test
    void invalid_rule_is_rejected() throws Exception {
        var itemId = createStock(10);

        mockMvc.perform(put("/api/reorder-rules/{itemId}", itemId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"reorderThreshold":5,"targetQuantity":5}
                                """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.detail").value("Target quantity must be greater than reorder threshold"));
    }

    @Test
    void unknown_stock_item_is_not_found() throws Exception {
        mockMvc.perform(get("/api/stock/MISSING-ITEM"))
                .andExpect(status().isNotFound());
    }

    @Test
    void completing_request_replenishes_stock_and_allows_a_later_reorder() throws Exception {
        var itemId = createStock(10);
        putRule(itemId, 5, 10);
        consume(itemId, 7);
        var requestId = findOpenRequestId(itemId);

        mockMvc.perform(post("/api/reorders/{requestId}/complete", requestId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("COMPLETED"));

        mockMvc.perform(get("/api/stock/{itemId}", itemId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.availableQuantity").value(10));

        consume(itemId, 6);
        mockMvc.perform(get("/api/reorders/{requestId}", requestId))
                .andExpect(status().isOk());
        mockMvc.perform(get("/api/reorders"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[?(@.itemId == '%s' && @.status == 'OPEN')]".formatted(itemId))
                        .value(org.hamcrest.Matchers.hasSize(1)));
    }

    private String createStock(int quantity) {
        var itemId = "HTTP-ITEM-%04d".formatted(ITEM_SEQUENCE.incrementAndGet());
        stockRepository.save(new StockItem(itemId, quantity));
        return itemId;
    }

    private void putRule(String itemId, int threshold, int target) throws Exception {
        mockMvc.perform(put("/api/reorder-rules/{itemId}", itemId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"reorderThreshold":%d,"targetQuantity":%d}
                                """.formatted(threshold, target)))
                .andExpect(status().isOk());
    }

    private void consume(String itemId, int quantity) throws Exception {
        mockMvc.perform(post("/api/stock/{itemId}/consume", itemId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"quantity":%d}
                                """.formatted(quantity)))
                .andExpect(status().isOk());
    }

    private String findOpenRequestId(String itemId) throws Exception {
        var result = mockMvc.perform(get("/api/reorders"))
                .andExpect(status().isOk())
                .andReturn();
        var json = result.getResponse().getContentAsString();
        var matcher = java.util.regex.Pattern.compile(
                "\\{\"id\":\"([^\"]+)\",\"itemId\":\"" + java.util.regex.Pattern.quote(itemId) + "\",\"quantity\":\\d+,\"availableQuantityAtTrigger\":\\d+,\"status\":\"OPEN\"\\}")
                .matcher(json);
        if (!matcher.find()) {
            throw new AssertionError("No open reorder request found for item " + itemId + " in " + json);
        }
        return matcher.group(1);
    }
}
