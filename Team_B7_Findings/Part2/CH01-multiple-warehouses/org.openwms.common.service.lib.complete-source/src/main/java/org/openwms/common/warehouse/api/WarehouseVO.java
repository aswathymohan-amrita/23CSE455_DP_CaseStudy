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
package org.openwms.common.warehouse.api;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import org.springframework.hateoas.RepresentationModel;

import java.io.Serializable;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class WarehouseVO extends RepresentationModel<WarehouseVO> implements Serializable {

    public static final String MEDIA_TYPE = "application/vnd.openwms.common.warehouse-v1+json";

    @JsonProperty("pKey")
    private String pKey;

    @NotBlank
    @Size(max = 32)
    @JsonProperty("code")
    private String code;

    @NotBlank
    @Size(max = 255)
    @JsonProperty("name")
    private String name;

    public WarehouseVO() { }

    public WarehouseVO(String code, String name) {
        this.code = code;
        this.name = name;
    }

    public String getpKey() {
        return pKey;
    }

    public void setpKey(String pKey) {
        this.pKey = pKey;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
