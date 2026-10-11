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
package org.openwms.common.warehouse.impl;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import org.ameba.annotation.Measured;
import org.ameba.annotation.TxService;
import org.ameba.exception.NotFoundException;
import org.ameba.exception.ResourceExistsException;
import org.ameba.i18n.Translator;
import org.openwms.common.warehouse.Warehouse;
import org.openwms.common.warehouse.WarehouseService;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.validation.annotation.Validated;

import java.util.List;
import java.util.Optional;

import static org.openwms.common.CommonMessageCodes.WAREHOUSE_CODE_EXISTS;
import static org.openwms.common.CommonMessageCodes.WAREHOUSE_NOT_FOUND;

@Validated
@TxService
class WarehouseServiceImpl implements WarehouseService {

    private final WarehouseRepository repository;
    private final Translator translator;

    WarehouseServiceImpl(WarehouseRepository repository, Translator translator) {
        this.repository = repository;
        this.translator = translator;
    }

    @Override
    @Measured
    public @NotNull Warehouse create(@NotNull @Valid Warehouse warehouse) {
        if (repository.findByCode(warehouse.getCode()).isPresent()) {
            throw new ResourceExistsException(translator, WAREHOUSE_CODE_EXISTS, new String[]{warehouse.getCode()}, warehouse.getCode());
        }
        return repository.save(warehouse);
    }

    @Override
    @Measured
    @Transactional(readOnly = true)
    public @NotNull List<Warehouse> findAll() {
        return repository.findAll();
    }

    @Override
    @Measured
    @Transactional(readOnly = true)
    public Optional<Warehouse> findByCode(@NotBlank String code) {
        return repository.findByCode(code);
    }

    @Override
    @Measured
    @Transactional(readOnly = true)
    public @NotNull Warehouse findByCodeOrThrow(@NotBlank String code) {
        return repository.findByCode(code)
                .orElseThrow(() -> new NotFoundException(translator, WAREHOUSE_NOT_FOUND, new String[]{code}, code));
    }
}
