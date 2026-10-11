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
package org.openwms.common.warehouse;

import org.ameba.exception.NotFoundException;
import org.ameba.exception.ResourceExistsException;
import org.junit.jupiter.api.Test;
import org.openwms.common.CommonApplicationTest;
import org.springframework.beans.factory.annotation.Autowired;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@CommonApplicationTest
class WarehouseServiceImplIT {

    @Autowired
    private WarehouseService warehouseService;

    @Test
    void creates_and_retrieves_a_warehouse() {
        var created = warehouseService.create(new Warehouse("NEW_WH", "New warehouse"));

        assertThat(created.getCode()).isEqualTo("NEW_WH");
        assertThat(warehouseService.findByCode("NEW_WH")).contains(created);
    }

    @Test
    void rejects_a_duplicate_warehouse_code() {
        warehouseService.create(new Warehouse("DUP_WH", "First warehouse"));

        assertThatThrownBy(() -> warehouseService.create(new Warehouse("DUP_WH", "Duplicate warehouse")))
                .isInstanceOf(ResourceExistsException.class)
                .hasMessageContaining("already exists");
    }

    @Test
    void rejects_an_unknown_warehouse_code() {
        assertThatThrownBy(() -> warehouseService.findByCodeOrThrow("UNKNOWN"))
                .isInstanceOf(NotFoundException.class)
                .hasMessageContaining("does not exist");
    }
}
