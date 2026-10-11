# CH03 Automatic Stock-Reorder Rules

## Scope

This is a separate Spring Boot reference implementation for the CH03 case study. The canonical current OpenWMS Inventory repository is inaccessible/private in this environment. No claims are made about its source, API, commits, tests, or behavior.

The implementation is inspired by the warehouse-management architecture used in this case study, not by a direct modification of canonical OpenWMS Inventory.

## Requirement

Add per-stock-item reorder threshold/target rules and automatically create a reorder recommendation when stock consumption brings stock to or below its configured threshold.

## BEFORE architecture

Commit `e9ad4c171771f12865de763b7f99e909b2539c47` contains simple in-memory stock management:

`StockController -> StockService.consume -> StockRepository -> StockItem.consume`

Stock consumption updates available quantity and does not create reorder requests.

## AFTER architecture

`StockController -> StockService.consume -> StockRepository -> StockItem.consume`

After the stock decrement, `StockService` invokes `ReorderService.evaluate(itemId)`. `ReorderService` reads current stock and a `ReorderRule` through `StockRepository` and `ReorderRuleRepository`, checks for an existing OPEN request using `ReorderRequestRepository`, then creates or reuses a `ReorderRequest`. `ReorderController` exposes request evaluation, lookup, listing, and completion. Completing a request replenishes its stock quantity and changes its status to COMPLETED.

`ReorderRuleController` creates/updates and reads the per-item threshold/target rule. The class relationships are captured in [CH03-class-diagram.puml](./CH03-class-diagram.puml).

## Reorder rule

A reorder is created only when both conditions hold:

```text
availableQuantity <= reorderThreshold
AND
availableQuantity < targetQuantity
```

The requested replenishment quantity is:

```text
reorderQuantity = targetQuantity - availableQuantity
```

Example: with available quantity `3`, threshold `5`, and target `10`, evaluation creates an OPEN request for `7`.

Rules reject blank item IDs, negative thresholds, and targets less than or equal to the threshold. This keeps the target above the reorder trigger level.

## Duplicate prevention

Before creating a new request, `ReorderService.evaluate` looks for an existing OPEN request for the same item. If present, that same request is returned rather than creating a duplicate. Evaluation is synchronized inside the service to serialize evaluations in this single-process in-memory reference implementation.

`POST /api/reorders/{requestId}/complete` adds the request quantity back to the associated stock item and marks the request COMPLETED. After that, a later low-stock evaluation can create a distinct request. Repeating completion for a completed request is rejected.

## API

| Method | Path | Behavior |
|--------|------|----------|
| `GET` | `/api/stock/{itemId}` | Return current stock, or 404 if unknown |
| `POST` | `/api/stock/{itemId}/consume` | Consume positive quantity, then automatically evaluate configured reorder rule |
| `PUT` | `/api/reorder-rules/{itemId}` | Create/update rule with `reorderThreshold` and `targetQuantity` |
| `GET` | `/api/reorder-rules/{itemId}` | Return configured rule |
| `POST` | `/api/reorders/evaluate/{itemId}` | Explicitly evaluate; 200 with created/reused request or 204 when no reorder is needed |
| `GET` | `/api/reorders` | List all requests |
| `GET` | `/api/reorders/{requestId}` | Get one request |
| `POST` | `/api/reorders/{requestId}/complete` | Replenish stock and complete the request |

Example rule:

```json
{
  "reorderThreshold": 5,
  "targetQuantity": 10
}
```

Example stock consumption:

```json
{
  "quantity": 7
}
```

Responses use `200 OK` for successful lookup/updates/evaluation and completion, `204 No Content` if evaluation finds no reorder condition, `400 Bad Request` for invalid rules or quantities, `404 Not Found` for unknown stock, rule, or request, and `409 Conflict` for insufficient stock or invalid repeated completion.

## Files created by the AFTER evolution

- `CH03-class-diagram.puml`
- `CH03_EVIDENCE.md`
- `src/main/java/org/openwms/casestudy/ch03/controller/ReorderController.java`
- `src/main/java/org/openwms/casestudy/ch03/controller/ReorderExceptionHandler.java`
- `src/main/java/org/openwms/casestudy/ch03/controller/ReorderRuleController.java`
- `src/main/java/org/openwms/casestudy/ch03/domain/ReorderRequest.java`
- `src/main/java/org/openwms/casestudy/ch03/domain/ReorderRule.java`
- `src/main/java/org/openwms/casestudy/ch03/domain/ReorderStatus.java`
- `src/main/java/org/openwms/casestudy/ch03/exception/InsufficientStockException.java`
- `src/main/java/org/openwms/casestudy/ch03/exception/InvalidReorderRuleException.java`
- `src/main/java/org/openwms/casestudy/ch03/exception/InvalidReorderStatusException.java`
- `src/main/java/org/openwms/casestudy/ch03/exception/InvalidStockQuantityException.java`
- `src/main/java/org/openwms/casestudy/ch03/exception/ReorderRequestNotFoundException.java`
- `src/main/java/org/openwms/casestudy/ch03/exception/ReorderRuleNotFoundException.java`
- `src/main/java/org/openwms/casestudy/ch03/exception/StockNotFoundException.java`
- `src/main/java/org/openwms/casestudy/ch03/repository/InMemoryReorderRequestRepository.java`
- `src/main/java/org/openwms/casestudy/ch03/repository/InMemoryReorderRuleRepository.java`
- `src/main/java/org/openwms/casestudy/ch03/repository/ReorderRequestRepository.java`
- `src/main/java/org/openwms/casestudy/ch03/repository/ReorderRuleRepository.java`
- `src/main/java/org/openwms/casestudy/ch03/service/ReorderService.java`
- `src/test/java/org/openwms/casestudy/ch03/controller/StockReorderControllerTest.java`
- `src/test/java/org/openwms/casestudy/ch03/domain/ReorderRuleTest.java`
- `src/test/java/org/openwms/casestudy/ch03/service/ReorderServiceTest.java`

`.gitignore` and `pom.xml` were established as part of the BEFORE project baseline, not added by the AFTER evolution.

## Files modified

Relative to the BEFORE commit:

- `src/main/java/org/openwms/casestudy/ch03/controller/StockController.java` — stock lookup and validation; consumes remain the external stock-change operation.
- `src/main/java/org/openwms/casestudy/ch03/domain/StockItem.java` — typed validation failures and replenishment operation used on completion.
- `src/main/java/org/openwms/casestudy/ch03/service/StockService.java` — invokes rule evaluation after successful consumption.
- `src/test/java/org/openwms/casestudy/ch03/service/StockServiceTest.java` — uses the evolved service wiring and typed unknown-item exception.

No files were deleted.

## Acceptance criteria

| ID | Acceptance criterion | Result |
|----|----------------------|--------|
| CH03-AC1 | Stock above threshold does not create a reorder | PASS |
| CH03-AC2 | Stock equal to threshold creates a reorder | PASS |
| CH03-AC3 | Stock below threshold creates a reorder | PASS |
| CH03-AC4 | Reorder quantity is target quantity minus available quantity | PASS |
| CH03-AC5 | Repeated evaluation while an OPEN request exists reuses it | PASS |
| CH03-AC6 | Negative threshold and invalid target rules are rejected | PASS |
| CH03-AC7 | Completing a request replenishes stock and clears its OPEN status | PASS |
| CH03-AC8 | A later low-stock condition after completion creates a new request | PASS |
| CH03-AC9 | Stock consumption automatically evaluates the configured rule | PASS |
| CH03-AC10 | Unknown stock is rejected | PASS |
| CH03-AC11 | Reorder requests can be retrieved individually and listed | PASS |

## Tests

The BEFORE source state passed:

```powershell
mvn.cmd -DforkCount=0 test
```

Result: `BUILD SUCCESS`; 2 tests, 0 failures, 0 errors, 0 skipped.

The focused AFTER test command is:

```powershell
mvn.cmd -DforkCount=0 -Dtest=ReorderRuleTest,ReorderServiceTest,StockServiceTest,StockReorderControllerTest test
```

The focused AFTER run passed: 19 tests, 0 failures, 0 errors, 0 skipped.

Full AFTER verification passed: `mvn.cmd -DforkCount=0 verify` reported `BUILD SUCCESS`; 19 tests, 0 failures, 0 errors, 0 skipped. The final `git diff --check` reported no whitespace errors.

## Metrics

Java LOC is the count of physical lines in all Java source and test files (including blank/comment lines). BEFORE was measured from its committed tree; AFTER from the final Java tree. Source and test-file counts are measured from `src/main/java` and `src/test/java`.

| State | Production Java files | Test Java files | Total Java files | Java LOC | Test cases |
|-------|-----------------------|-----------------|------------------|----------|------------|
| BEFORE | 6 | 1 | 7 | 169 | 2 |
| AFTER | 24 | 4 | 28 | 978 | 19 |

Reproduction: use `git ls-tree -r --name-only e9ad4c171771f12865de763b7f99e909b2539c47` and `git show <commit>:<path>` to count BEFORE Java paths/lines; recursively enumerate `*.java` under `src` and count physical lines to measure AFTER. Surefire test totals are reported directly by Maven.

## Design-pattern impact

No new GoF pattern was introduced by CH03.

`ReorderRule` encapsulates one explicit threshold/target predicate and its quantity calculation. There are no interchangeable reorder algorithms or policy implementations, so this is not Strategy. Spring MVC, dependency injection, and repository interfaces are architectural/framework mechanisms, not claimed as new GoF patterns.

## Sequence description

1. A client consumes stock through `StockController`.
2. `StockService` changes stock through `StockItem.consume` and saves it through `StockRepository`.
3. `StockService` calls `ReorderService.evaluate(itemId)`.
4. `ReorderService` loads current stock and its configured rule.
5. An existing OPEN request is returned if present; otherwise, the rule is evaluated.
6. If the stock satisfies the reorder conditions, `ReorderService` calculates the target-stock gap and saves a new OPEN request through `ReorderRequestRepository`.
7. Completion replenishes stock and marks the request COMPLETED.

## Limitations

The implementation is a reference case-study implementation and is not a modification of the restricted canonical OpenWMS Inventory repository.

Stock, rules, requests, and request IDs are in memory; data is lost on restart. This is not a production persistence or distributed-locking implementation and does not integrate suppliers, purchase orders, ERP, or external messaging. Synchronization only serializes operations within the single running application process.

## Reproducibility

Requirements: Java 17 or later and Maven 3.9.x.

From `CH03-stock-reorder/`, run:

```powershell
mvn.cmd -DforkCount=0 test
mvn.cmd -DforkCount=0 verify
```

## Re-audit note (2026-10-11)

- The BEFORE and AFTER commit IDs cited above come from the original local project repository. That Git history was not copied into `Team_B9_DP`, so the commits cannot be checked out from the submission repository, and the BEFORE metrics cannot be reproduced from it. Only the AFTER source tree is published here.
- The AFTER tree in this repository was re-measured and matches the table above exactly (file counts, physical Java LOC, and the number of `@Test` methods).
- Maven could not be re-run during the re-audit because the audit environment blocked Maven Central; the recorded `BUILD SUCCESS` results are the team's original runs.
- Test-quality observation: `StockServiceTest.consumption_reduces_stock_without_creating_a_reorder` configures no reorder rule and asserts only the remaining quantity; it does not assert that no reorder request was created. The "no reorder" behaviour is covered by `ReorderRuleTest.stock_above_threshold_does_not_require_reorder` and `ReorderServiceTest.stock_above_threshold_does_not_create_a_request`.
