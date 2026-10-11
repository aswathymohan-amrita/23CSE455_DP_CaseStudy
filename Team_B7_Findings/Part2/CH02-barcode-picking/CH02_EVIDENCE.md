# CH02 Barcode-Based Picking

## Scope

This is a standalone Spring Boot reference implementation for the CH02 case study, inspired by the separation of responsibilities requested for the study. The canonical OpenWMS Picking repository is inaccessible in this workspace, so no claims are made about its source, APIs, commits, tests, or existing behavior.

## Requirement

Introduce barcode-based picking: resolve an actual barcode to stock, validate the item and requested quantity, pick the quantity, and return the updated stock result.

## BEFORE architecture

The baseline commit `5ca90cc12be1141be47cb6e6bdf3ca26efe636bd` implements a functional direct-item-identifier flow:

`PickingController -> PickingService.pickByItemId(itemId, quantity) -> StockRepository.findById(itemId) -> StockItem.pick(quantity)`

It exposes `POST /api/picking/item`; no barcode lookup or barcode endpoint existed in the baseline.

## AFTER architecture

The barcode workflow is:

`PickingController.pickByBarcode -> PickingService.pickByBarcode -> BarcodeResolver.resolve(barcode) -> StockRepository.findByBarcode -> StockItem`

After resolution, `PickingService` applies quantity checks and calls `StockItem.pick`, persists the changed item through `StockRepository.save`, and returns a `PickingResult`. The service also depends directly on `StockRepository` for the separate direct-item-ID flow and for saving picked stock; the relationships are not a strictly linear chain.

`StockItem` has stable item and barcode values, product and location information, available quantity, and availability state. The in-memory repository seeds barcode `8901234567890` for product `ITEM-001`, location `A-01-01`, with quantity 10.

## Files created

Project/build:

- `.gitignore`
- `CH02_EVIDENCE.md`
- `pom.xml`

Production Java:

- `src/main/java/org/openwms/casestudy/ch02/PickingApplication.java`
- `src/main/java/org/openwms/casestudy/ch02/controller/PickingController.java`
- `src/main/java/org/openwms/casestudy/ch02/controller/PickingExceptionHandler.java`
- `src/main/java/org/openwms/casestudy/ch02/domain/PickingRequest.java`
- `src/main/java/org/openwms/casestudy/ch02/domain/PickingResult.java`
- `src/main/java/org/openwms/casestudy/ch02/domain/StockItem.java`
- `src/main/java/org/openwms/casestudy/ch02/exception/BarcodeNotFoundException.java`
- `src/main/java/org/openwms/casestudy/ch02/exception/InsufficientStockException.java`
- `src/main/java/org/openwms/casestudy/ch02/exception/InvalidPickingQuantityException.java`
- `src/main/java/org/openwms/casestudy/ch02/exception/StockUnavailableException.java`
- `src/main/java/org/openwms/casestudy/ch02/repository/InMemoryStockRepository.java`
- `src/main/java/org/openwms/casestudy/ch02/repository/StockRepository.java`
- `src/main/java/org/openwms/casestudy/ch02/service/BarcodeResolver.java`
- `src/main/java/org/openwms/casestudy/ch02/service/PickingService.java`

Tests:

- `src/test/java/org/openwms/casestudy/ch02/controller/PickingControllerTest.java`
- `src/test/java/org/openwms/casestudy/ch02/service/BarcodeResolverTest.java`
- `src/test/java/org/openwms/casestudy/ch02/service/PickingServiceTest.java`

## Files modified

Relative to the BEFORE commit:

- `src/main/java/org/openwms/casestudy/ch02/controller/PickingController.java` — retained the direct item route and added the barcode route.
- `src/main/java/org/openwms/casestudy/ch02/domain/PickingResult.java` — added the resolved barcode to the picking result.
- `src/main/java/org/openwms/casestudy/ch02/domain/StockItem.java` — added explicit invalid-quantity, unavailable-stock, and insufficient-stock rejection while reducing quantity after a successful pick.
- `src/main/java/org/openwms/casestudy/ch02/repository/InMemoryStockRepository.java` — added barcode lookup.
- `src/main/java/org/openwms/casestudy/ch02/repository/StockRepository.java` — added the barcode lookup contract.
- `src/main/java/org/openwms/casestudy/ch02/service/PickingService.java` — added barcode resolution and kept direct-ID picking as a distinct operation.
- `src/test/java/org/openwms/casestudy/ch02/service/PickingServiceTest.java` — expanded service behavior coverage.

No files were deleted. No existing CORE, CH01, or canonical Picking repository files were modified.

## API

`POST /api/picking/barcode`

Request:

```json
{
  "barcode": "8901234567890",
  "quantity": 2
}
```

Successful response (`200 OK`):

```json
{
  "itemId": "STOCK-001",
  "barcode": "8901234567890",
  "productCode": "ITEM-001",
  "quantityPicked": 2,
  "location": "A-01-01",
  "remainingQuantity": 8
}
```

Status mapping:

- `200 OK` — stock was picked successfully.
- `400 Bad Request` — invalid request or quantity below one.
- `404 Not Found` — barcode does not resolve to stock.
- `409 Conflict` — stock is unavailable or the requested quantity exceeds available stock.

The separate baseline-compatible direct-ID operation remains at `POST /api/picking/item`.

## Acceptance criteria

| ID | Acceptance criterion | Result |
|----|----------------------|--------|
| CH02-AC1 | Valid barcode resolves to stock and picking succeeds | PASS |
| CH02-AC2 | Unknown barcode is rejected without creating stock | PASS |
| CH02-AC3 | Unavailable/out-of-stock stock cannot be picked | PASS |
| CH02-AC4 | Quantity above available stock is rejected | PASS |
| CH02-AC5 | Successful pick decreases available quantity and returns the remaining quantity | PASS |
| CH02-AC6 | Zero and negative quantities are rejected | PASS |
| CH02-AC7 | Direct item-ID picking remains a separate working flow | PASS |
| CH02-AC8 | MVC endpoint returns documented success and error statuses | PASS |

## Tests

Commands run from this project directory using Maven 3.9.9:

```powershell
mvn.cmd -DforkCount=0 test
mvn.cmd -DforkCount=0 -Dtest=BarcodeResolverTest,PickingServiceTest,PickingControllerTest test
mvn.cmd -DforkCount=0 verify
```

The BEFORE direct-ID implementation passed `mvn.cmd -DforkCount=0 test`: 1 test, 0 failures, 0 errors, 0 skipped.

The focused AFTER test run passed: 14 tests, 0 failures, 0 errors, 0 skipped.

Full AFTER verification passed: `mvn.cmd -DforkCount=0 verify` completed with `BUILD SUCCESS`; Surefire reported 14 tests, 0 failures, 0 errors, 0 skipped.

## Metrics

Metrics count Java files and physical Java source lines (production plus test source); LOC includes blank lines and comments. BEFORE was measured from the committed baseline tree; AFTER from the checked-out source tree.

| State | Production Java files | Test Java files | Total Java files | Java LOC | Test cases |
|-------|-----------------------|-----------------|------------------|----------|------------|
| BEFORE | 7 | 1 | 8 | 197 | 1 |
| AFTER | 14 | 3 | 17 | 526 | 14 |

Reproduction method: list baseline Java paths using `git ls-tree -r --name-only 5ca90cc12be1141be47cb6e6bdf3ca26efe636bd`, count lines from each `git show <baseline>:<path>`, and count AFTER Java files under `src` with recursive `Get-ChildItem -Filter '*.java'`; physical lines were counted with `.NET [IO.File]::ReadAllLines(path).Length`. The test counts come from Maven Surefire summaries, not source-text estimates.

## Design-pattern impact

No new GoF pattern was introduced by this evolution.

The code has MVC-style HTTP separation (`PickingController` and `PickingService`) and a repository abstraction (`StockRepository`), which are application/framework architecture mechanisms rather than claims of new GoF patterns. `BarcodeResolver` is a focused collaborator that performs barcode lookup; its presence alone does not make this a GoF pattern.

## UML / class relationships

- `PickingController` depends on `PickingService` for both HTTP operations.
- `PickingService` depends on `BarcodeResolver` for barcode resolution and on `StockRepository` for direct-ID lookup and saving.
- `BarcodeResolver` depends on `StockRepository` to find a stock item by barcode.
- `StockRepository` returns and saves `StockItem` instances.
- `PickingService` validates and picks the resolved `StockItem`, then constructs `PickingResult`.
- `PickingExceptionHandler` maps known picking exceptions to HTTP error responses.

## Limitations

This reference project uses an in-memory repository and a deterministic demo item; state is not durable across restarts and it is not a production persistence/concurrency design. It does not integrate barcode hardware, a database, or external services.

The implementation is not a modification of the restricted canonical OpenWMS Picking repository.

## Reproducibility

Requirements: Java 17 or later and Maven 3.9.x.

Run the full tests and verification from `CH02-barcode-picking/`:

```powershell
mvn.cmd test
mvn.cmd verify
```

## Re-audit note (2026-10-11)

- The BEFORE and AFTER commit IDs cited above come from the original local project repository. That Git history was not copied into `Team_B9_DP`, so the commits cannot be checked out from the submission repository, and the BEFORE metrics cannot be reproduced from it. Only the AFTER source tree is published here.
- The AFTER tree in this repository was re-measured and matches the table above exactly (file counts, physical Java LOC, and the number of `@Test` methods).
- Maven could not be re-run during the re-audit because the audit environment blocked Maven Central; the recorded `BUILD SUCCESS` results are the team's original runs.
