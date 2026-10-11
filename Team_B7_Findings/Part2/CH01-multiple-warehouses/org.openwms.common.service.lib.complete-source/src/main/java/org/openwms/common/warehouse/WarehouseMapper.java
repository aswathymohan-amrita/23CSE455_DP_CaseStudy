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
import org.ameba.i18n.Translator;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.openwms.common.warehouse.api.WarehouseVO;
import org.springframework.beans.factory.annotation.Autowired;

import static org.openwms.common.CommonMessageCodes.WAREHOUSE_NOT_FOUND;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public abstract class WarehouseMapper {

    private WarehouseService warehouseService;
    private Translator translator;

    @Autowired
    public void setWarehouseService(WarehouseService warehouseService) {
        this.warehouseService = warehouseService;
    }

    @Autowired
    public void setTranslator(Translator translator) {
        this.translator = translator;
    }

    public Warehouse convertFromCode(String code) {
        if (code == null) {
            return null;
        }
        return warehouseService.findByCode(code)
                .orElseThrow(() -> new NotFoundException(translator, WAREHOUSE_NOT_FOUND, new String[]{code}, code));
    }

    @Mapping(target = "pKey", source = "persistentKey")
    public abstract WarehouseVO convertToVO(Warehouse warehouse);
}
