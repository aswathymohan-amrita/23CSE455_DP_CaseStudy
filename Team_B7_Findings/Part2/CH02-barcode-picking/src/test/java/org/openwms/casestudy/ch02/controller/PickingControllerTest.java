package org.openwms.casestudy.ch02.controller;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openwms.casestudy.ch02.domain.StockItem;
import org.openwms.casestudy.ch02.repository.InMemoryStockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class PickingControllerTest {

    private static final String BARCODE = "8901234567890";
    private static final String ITEM_ID = "STOCK-001";

    @Autowired
    private MockMvc mockMvc;
    @Autowired
    private InMemoryStockRepository stockRepository;

    @BeforeEach
    void resetDemoStock() {
        stockRepository.save(new StockItem(ITEM_ID, BARCODE, "ITEM-001", "A-01-01", 10, true));
    }

    @Test
    void post_valid_barcode_picks_stock_and_returns_result() throws Exception {
        mockMvc.perform(post("/api/picking/barcode")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"barcode":"8901234567890","quantity":2}
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.barcode").value(BARCODE))
                .andExpect(jsonPath("$.productCode").value("ITEM-001"))
                .andExpect(jsonPath("$.quantityPicked").value(2))
                .andExpect(jsonPath("$.location").value("A-01-01"))
                .andExpect(jsonPath("$.remainingQuantity").value(8));
    }

    @Test
    void post_unknown_barcode_returns_not_found() throws Exception {
        mockMvc.perform(post("/api/picking/barcode")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"barcode":"UNKNOWN","quantity":1}
                                """))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.detail").value("No stock item found for barcode: UNKNOWN"));
    }

    @Test
    void post_excessive_quantity_returns_conflict() throws Exception {
        mockMvc.perform(post("/api/picking/barcode")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"barcode":"8901234567890","quantity":11}
                                """))
                .andExpect(status().isConflict());
    }

    @Test
    void post_zero_quantity_returns_bad_request() throws Exception {
        mockMvc.perform(post("/api/picking/barcode")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"barcode":"8901234567890","quantity":0}
                                """))
                .andExpect(status().isBadRequest());
    }

    @Test
    void post_unavailable_stock_returns_conflict() throws Exception {
        stockRepository.save(new StockItem("STOCK-OUT", "BAR-OUT", "ITEM-OUT", "A-01-02", 0, false));

        mockMvc.perform(post("/api/picking/barcode")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"barcode":"BAR-OUT","quantity":1}
                                """))
                .andExpect(status().isConflict());
    }

    @Test
    void direct_item_id_endpoint_remains_separate_and_available() throws Exception {
        mockMvc.perform(post("/api/picking/item")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"itemId":"STOCK-001","quantity":1}
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.itemId").value(ITEM_ID))
                .andExpect(jsonPath("$.remainingQuantity").value(9));
    }
}
