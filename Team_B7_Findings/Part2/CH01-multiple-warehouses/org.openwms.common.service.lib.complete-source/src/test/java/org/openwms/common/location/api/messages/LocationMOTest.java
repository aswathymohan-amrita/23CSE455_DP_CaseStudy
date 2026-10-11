/*
 * Copyright 2005-2025 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.openwms.common.location.api.messages;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class LocationMOTest {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Test
    void legacy_nine_argument_constructor_preserves_null_warehouse() {
        var message = new LocationMO("pKey", "account", "id", "plc", "erp", "group", true, false, 0);

        assertThat(message.warehouseCode()).isNull();
    }

    @Test
    void warehouse_code_is_preserved_by_json_serialization() throws Exception {
        var message = LocationMO.ofId("WH1", "AREA/AISLE/X/Y/Z");

        var json = objectMapper.writeValueAsString(message);
        var restored = objectMapper.readValue(json, LocationMO.class);

        assertThat(json).contains("\"warehouseCode\":\"WH1\"");
        assertThat(restored.warehouseCode()).isEqualTo("WH1");
        assertThat(restored.id()).isEqualTo("AREA/AISLE/X/Y/Z");
    }
}
