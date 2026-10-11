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
package org.openwms.common.transport.commands;

import org.ameba.exception.ResourceExistsException;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openwms.common.CommonApplicationTest;
import org.openwms.common.TestData;
import org.openwms.common.location.Location;
import org.openwms.common.location.LocationPK;
import org.openwms.common.location.LocationService;
import org.openwms.common.location.api.messages.LocationMO;
import org.openwms.common.transport.TransportUnit;
import org.openwms.common.transport.TransportUnitService;
import org.openwms.common.transport.api.commands.TUCommand;
import org.openwms.common.transport.api.messages.TransportUnitMO;
import org.openwms.common.transport.api.messages.TransportUnitTypeMO;
import org.openwms.common.transport.barcode.BarcodeGenerator;
import org.openwms.common.warehouse.WarehouseService;
import org.springframework.beans.factory.annotation.Autowired;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@CommonApplicationTest
class TransportUnitCommandHandlerIT {

    private static final String DUPLICATE_LOCATION_ID = "DUPL/0001/0001/0001/0001";

    @Autowired
    private TransportUnitCommandHandler handler;
    @Autowired
    private TransportUnitService transportUnitService;
    @Autowired
    private LocationService locationService;
    @Autowired
    private WarehouseService warehouseService;
    @Autowired
    private BarcodeGenerator barcodeGenerator;

    @BeforeEach
    void configureBarcodeGenerator() {
        System.setProperty("org.openwms.common.transport.BarcodeFormatProvider", "org.openwms.common.transport.ConfiguredBarcodeFormat");
        System.setProperty("owms.common.barcode.pattern", "%s");
        System.setProperty("owms.common.barcode.padder", "0");
    }

    @AfterEach
    void resetBarcodeGenerator() {
        System.setProperty("org.openwms.common.transport.BarcodeFormatProvider", "");
        System.setProperty("owms.common.barcode.pattern", "");
        System.setProperty("owms.common.barcode.padder", "");
    }

    @Test
    void creates_transport_units_at_the_same_coordinates_in_the_requested_warehouses() {
        createDuplicateLocation();

        var warehouseOne = create("8101", TestData.WAREHOUSE_CODE, DUPLICATE_LOCATION_ID);
        var warehouseTwo = create("8102", TestData.SECOND_WAREHOUSE_CODE, DUPLICATE_LOCATION_ID);

        assertThat(warehouseOne.getActualLocation().getWarehouse().getCode()).isEqualTo(TestData.WAREHOUSE_CODE);
        assertThat(warehouseTwo.getActualLocation().getWarehouse().getCode()).isEqualTo(TestData.SECOND_WAREHOUSE_CODE);
    }

    @Test
    void creates_without_warehouse_when_the_coordinate_is_unique() {
        var transportUnit = create("8103", null, TestData.LOCATION_ID_EXT);

        assertThat(transportUnit.getActualLocation().getWarehouse().getCode()).isEqualTo(TestData.WAREHOUSE_CODE);
    }

    @Test
    void rejects_unqualified_creation_when_the_coordinate_is_ambiguous() {
        createDuplicateLocation();

        assertThatThrownBy(() -> create("8104", null, DUPLICATE_LOCATION_ID))
                .isInstanceOf(ResourceExistsException.class)
                .hasMessageContaining("more than one warehouse");
    }

    private TransportUnit create(String barcode, String warehouseCode, String locationId) {
        var location = warehouseCode == null
                ? LocationMO.ofId(locationId)
                : LocationMO.ofId(warehouseCode, locationId);
        handler.handle(TUCommand.newBuilder(TUCommand.Type.CREATE)
                .withTransportUnit(TransportUnitMO.newBuilder()
                        .withBarcode(barcode)
                        .withTransportUnitType(TransportUnitTypeMO.newBuilder()
                                .type(TestData.TUT_TYPE_PALLET)
                                .build())
                        .withActualLocation(location)
                        .build())
                .build());
        return transportUnitService.findByBarcode(barcode);
    }

    private void createDuplicateLocation() {
        locationService.create(Location.create(
                warehouseService.findByCodeOrThrow(TestData.WAREHOUSE_CODE),
                LocationPK.fromString(DUPLICATE_LOCATION_ID)));
        locationService.create(Location.create(
                warehouseService.findByCodeOrThrow(TestData.SECOND_WAREHOUSE_CODE),
                LocationPK.fromString(DUPLICATE_LOCATION_ID)));
    }
}
