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

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import org.ameba.integration.jpa.ApplicationEntity;
import org.springframework.util.Assert;

import java.io.Serializable;
import java.util.Objects;

/**
 * A Warehouse is a physical facility that owns a set of {@code Location}s.
 *
 * @author OpenWMS.org
 */
@Entity
@Table(name = Warehouse.TABLE, uniqueConstraints = @UniqueConstraint(name = "UC_WHS_CODE", columnNames = "C_CODE"))
public class Warehouse extends ApplicationEntity implements Serializable {

    public static final String TABLE = "COM_WAREHOUSE";

    @NotBlank
    @Size(max = 32)
    @Column(name = "C_CODE", nullable = false, updatable = false, length = 32)
    private String code;

    @NotBlank
    @Size(max = 255)
    @Column(name = "C_NAME", nullable = false, length = 255)
    private String name;

    protected Warehouse() { }

    public Warehouse(String code, String name) {
        Assert.hasText(code, "Warehouse code must not be blank");
        Assert.hasText(name, "Warehouse name must not be blank");
        this.code = code;
        this.name = name;
    }

    public String getCode() {
        return code;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        Assert.hasText(name, "Warehouse name must not be blank");
        this.name = name;
    }

    @Override
    public String toString() {
        return code;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Warehouse warehouse = (Warehouse) o;
        return Objects.equals(code, warehouse.code);
    }

    @Override
    public int hashCode() {
        return Objects.hash(code);
    }
}
