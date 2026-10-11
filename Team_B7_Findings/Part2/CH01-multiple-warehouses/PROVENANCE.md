# CH01 — Multiple warehouses: provenance and verification

CH01 is the recorded working-tree change to two separate public OpenWMS repositories. The original partial changed-file snapshots are preserved at `org.openwms.common.service.lib/` and `org.openwms.common.service/`. Separate `*.complete-source/` sibling directories contain the full eligible source/build/documentation snapshots, including unchanged Java support classes. No copied directory contains Git history.

| Repository | Upstream | Baseline/current HEAD at audit |
|---|---|---|
| `org.openwms.common.service.lib` | <https://github.com/openwms/org.openwms.common.service.lib> | `a6566d7a90364f8cb0e82ec013720b644926dffe` |
| `org.openwms.common.service` | <https://github.com/openwms/org.openwms.common.service> | `fc7edd4ffbe16de65d482b3a2d462d4d896b1998` |
| OpenWMS Core reference baseline | <https://github.com/openwms/org.openwms> | `9d263bf65ec75301e0302539ae7bf581412742b8` |

At the audit, CH01 changes were unstaged and uncommitted in the two original worktrees; Core was clean. No commit, merge, or deployment is claimed here. Consult the original repositories for complete working trees and Git state.

## Exact CH01 changed-file lists

Paths below are relative to the named original repository. The same CH01 changed paths remain present in both its partial evidence snapshot and its complete-source snapshot.

### `org.openwms.common.service.lib`

**31 tracked modified files**

```text
src/main/asciidoc/api.adoc
src/main/java/org/openwms/common/CommonMessageCodes.java
src/main/java/org/openwms/common/location/Location.java
src/main/java/org/openwms/common/location/LocationController.java
src/main/java/org/openwms/common/location/LocationMapper.java
src/main/java/org/openwms/common/location/LocationPK.java
src/main/java/org/openwms/common/location/LocationService.java
src/main/java/org/openwms/common/location/TargetController.java
src/main/java/org/openwms/common/location/WorkflowApi.java
src/main/java/org/openwms/common/location/api/LocationApi.java
src/main/java/org/openwms/common/location/api/LocationVO.java
src/main/java/org/openwms/common/location/api/TargetApi.java
src/main/java/org/openwms/common/location/api/events/TargetEvent.java
src/main/java/org/openwms/common/location/api/messages/LocationMO.java
src/main/java/org/openwms/common/location/impl/LocationRepository.java
src/main/java/org/openwms/common/location/impl/LocationServiceImpl.java
src/main/java/org/openwms/common/transport/TransportUnitController.java
src/main/java/org/openwms/common/transport/TransportUnitService.java
src/main/java/org/openwms/common/transport/api/TransportUnitApi.java
src/main/java/org/openwms/common/transport/commands/TransportUnitCommandHandler.java
src/main/java/org/openwms/common/transport/impl/TransportUnitServiceImpl.java
src/main/resources/META-INF/common-orm.xml
src/main/resources/META-INF/i18n/common.properties
src/test/java/org/openwms/common/TestData.java
src/test/java/org/openwms/common/location/LocationControllerDocumentation.java
src/test/java/org/openwms/common/location/LocationIT.java
src/test/java/org/openwms/common/location/LocationTest.java
src/test/java/org/openwms/common/location/impl/LocationServiceImplIT.java
src/test/java/org/openwms/common/transport/TransportUnitControllerDocumentation.java
src/test/java/org/openwms/common/transport/impl/TransportUnitServiceImplIT.java
src/test/resources/test.sql
```

**13 untracked CH01 files**

```text
src/main/asciidoc/9-warehouse.adoc
src/main/java/org/openwms/common/warehouse/Warehouse.java
src/main/java/org/openwms/common/warehouse/WarehouseController.java
src/main/java/org/openwms/common/warehouse/WarehouseMapper.java
src/main/java/org/openwms/common/warehouse/WarehouseService.java
src/main/java/org/openwms/common/warehouse/api/WarehouseApi.java
src/main/java/org/openwms/common/warehouse/api/WarehouseApiConstants.java
src/main/java/org/openwms/common/warehouse/api/WarehouseVO.java
src/main/java/org/openwms/common/warehouse/impl/WarehouseRepository.java
src/main/java/org/openwms/common/warehouse/impl/WarehouseServiceImpl.java
src/test/java/org/openwms/common/location/api/messages/LocationMOTest.java
src/test/java/org/openwms/common/transport/commands/TransportUnitCommandHandlerIT.java
src/test/java/org/openwms/common/warehouse/WarehouseServiceImplIT.java
```

### `org.openwms.common.service`

**2 tracked modified files**

```text
src/main/resources/META-INF/common-orm.xml
src/main/resources/import-DEMO.sql
```

No untracked CH01 files were reported for this repository at the recorded audit.

## Complete-source snapshot contents and exclusions

- `org.openwms.common.service.lib.complete-source/`: 276 files copied, including all 238 Java source/test files and the repository POM, Maven wrapper scripts/properties, README, `.gitignore`, and Apache-2.0 LICENSE.
- `org.openwms.common.service.complete-source/`: 69 files copied, including all 5 Java source/test files and the repository POM, Maven wrapper scripts/properties, README, `.gitignore`, Dockerfile, documentation, and Apache-2.0 LICENSE.
- Neither original repository contains a `NOTICE` file.
- `.git/`, `target/`, generated output, caches, and temporary files are omitted. There is no `.git` metadata in either copied tree.
- Credential-bearing or credential-like files were excluded from the copies: Library `.github/workflows/master-build.yml` and `src/test/resources/application.yml`; Service `.github/workflows/master-build.yml`, `doc/Config.groovy`, `doc/docToolchainConfig.groovy`, `doc/bin/upload.py`, `doc/bin/uploadAll.py`, `doc/scripts/publishToMediawiki.gradle`, `doc/scripts/publishToOpenProject.gradle`, and `src/main/resources/bootstrap.yml`. The original files were not changed.
- These are complete eligible source snapshots, not guaranteed standalone build workspaces: Git metadata and the listed configuration files are intentionally absent. No compilation or test run is claimed for these copies.

## Recorded full verification

- Library: cached Maven 3.9.9 `mvn.cmd -DforkCount=0 install`; exit 0, `BUILD SUCCESS`; 187 tests, 0 failures, 0 errors, 7 skipped.
- Common Service: cached Maven 3.9.9 `mvn.cmd -DforkCount=0 verify`; exit 0, `BUILD SUCCESS`; 1 test, 0 failures, 0 errors, 0 skipped; Failsafe reported no tests to run.
- `git diff --check` exited 0 in both CH01 repositories and Core.
- Both Maven invocations emitted the warning that `forkCount=0` may reduce test accuracy. The Library build also logged Asciidoctor errors for an unavailable generated snippet and invalid part structure, despite Maven's `BUILD SUCCESS`.

Production locations still require deployment-provided Warehouse mapping. No production migration/backfill, Flyway/Liquibase migration, deployment, or CH01 before/after LOC measurement is evidenced.

## Re-audit (2026-10-11)

The changed-file lists above were re-derived by comparing `org.openwms.common.service.lib.complete-source/` and `org.openwms.common.service.complete-source/` with fresh clones of the upstream repositories at the stated baselines. The result matches exactly: 31 modified and 13 new files in the Library (226 upstream Java files + 12 new = 238), and 2 modified files in Common Service. The partial snapshots are byte-identical to the complete-source copies, apart from a UTF-8 byte-order mark on the partial Common Service `README.md`.

### CH01 test methods (named in source)

The focused CH01 tests are identifiable by name in the snapshot; 18 test methods were added (245 `@Test` annotations upstream, 263 after).

| Acceptance criterion | Test method(s) |
|---|---|
| Same coordinates in different warehouses | `LocationTest.same_coordinates_in_different_warehouses_are_distinct_locations`; `LocationIT.shall_allow_same_coordinates_in_different_warehouses`; `LocationServiceImplIT.shall_allow_same_location_id_in_different_warehouses_and_find_by_warehouse` |
| Warehouse-qualified lookup / update | `TransportUnitServiceImplIT.update_with_warehouse_code_selects_the_requested_warehouse_for_duplicate_coordinates`; `TransportUnitCommandHandlerIT.creates_transport_units_at_the_same_coordinates_in_the_requested_warehouses` |
| Ambiguous unqualified lookup is rejected | `TransportUnitServiceImplIT.update_without_warehouse_code_rejects_an_ambiguous_coordinate`; `TransportUnitCommandHandlerIT.rejects_unqualified_creation_when_the_coordinate_is_ambiguous` |
| Unqualified lookup of a unique coordinate still works | `TransportUnitServiceImplIT.update_without_warehouse_code_resolves_a_unique_coordinate`; `TransportUnitCommandHandlerIT.creates_without_warehouse_when_the_coordinate_is_unique` |
| Unknown warehouse is rejected | `LocationServiceImplIT.shall_reject_location_with_unknown_warehouse`; `WarehouseServiceImplIT.rejects_an_unknown_warehouse_code` |
| Warehouse management | `WarehouseServiceImplIT.creates_and_retrieves_a_warehouse`; `WarehouseServiceImplIT.rejects_a_duplicate_warehouse_code` |
| API/message carry warehouse code | `LocationServiceImplIT.location_api_and_message_carry_warehouse_code`; `LocationMOTest.warehouse_code_is_preserved_by_json_serialization` |
| Legacy `LocationMO` constructor compatibility | `LocationMOTest.legacy_nine_argument_constructor_preserves_null_warehouse` |

**Correction:** "Duplicate coordinates within one warehouse are rejected" is enforced by the `UC_LOC_ID` unique constraint on (`C_WAREHOUSE`, `C_AREA`, `C_AISLE`, `C_X`, `C_Y`, `C_Z`) in `Location.java` (CH01 added `C_WAREHOUSE`; the baseline constraint covered only the five coordinate columns), but no test exercises that rejection. Its status is *enforced by schema constraint, not tested*. PLC/ERP global uniqueness is enforced by `UC_LOC_PLC_CODE` and `UC_LOC_ERP_CODE`, which CH01 left unchanged from the baseline; there is no dedicated CH01 test for it.

Maven could not be re-run during the re-audit (Maven Central was blocked in the audit environment); the 187/7 and 1/0 totals above are the team's recorded runs.
