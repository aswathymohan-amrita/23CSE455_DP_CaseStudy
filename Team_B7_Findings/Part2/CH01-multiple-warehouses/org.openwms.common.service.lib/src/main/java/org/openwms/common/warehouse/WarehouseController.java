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

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.ameba.http.MeasuredRestController;
import org.openwms.common.warehouse.api.WarehouseVO;
import org.openwms.core.http.AbstractWebController;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;

import static org.openwms.common.warehouse.api.WarehouseApiConstants.API_WAREHOUSES;
import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.linkTo;
import static org.springframework.hateoas.server.mvc.WebMvcLinkBuilder.methodOn;

@Validated
@MeasuredRestController
public class WarehouseController extends AbstractWebController {

    private final WarehouseService service;
    private final WarehouseMapper mapper;

    public WarehouseController(WarehouseService service, WarehouseMapper mapper) {
        this.service = service;
        this.mapper = mapper;
    }

    @PostMapping(value = API_WAREHOUSES, produces = WarehouseVO.MEDIA_TYPE)
    public ResponseEntity<WarehouseVO> create(@Valid @RequestBody WarehouseVO warehouse, HttpServletRequest request) {
        var created = service.create(new Warehouse(warehouse.getCode(), warehouse.getName()));
        var result = addSelfLink(mapper.convertToVO(created));
        return ResponseEntity.created(getLocationURIForCreatedResource(request, created.getPersistentKey()))
                .header(HttpHeaders.CONTENT_TYPE, WarehouseVO.MEDIA_TYPE)
                .body(result);
    }

    @GetMapping(value = API_WAREHOUSES, params = "code", produces = WarehouseVO.MEDIA_TYPE)
    public ResponseEntity<WarehouseVO> findByCode(@RequestParam("code") String code) {
        var warehouse = service.findByCodeOrThrow(code);
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_TYPE, WarehouseVO.MEDIA_TYPE)
                .body(addSelfLink(mapper.convertToVO(warehouse)));
    }

    private WarehouseVO addSelfLink(WarehouseVO result) {
        result.add(linkTo(methodOn(WarehouseController.class).findByCode(result.getCode())).withRel("warehouse-findbycode"));
        return result;
    }
}
