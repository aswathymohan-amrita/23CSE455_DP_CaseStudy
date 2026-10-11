# Human Verification Notes — Part 1

Reviewer: Student verification (identity omitted in publication copy)
Baseline: `9d263bf65ec75301e0302539ae7bf581412742b8`

## Observer
Confirmed by direct inspection of the EventBroker/EventDispatcher/EventListener/SimpleEventDispatcher collaboration. The dispatcher stores subscriptions and calls `EventListener.onEvent` for subscribed listeners.

## Composite
Confirmed by direct inspection of TreeNode/TreeNodeImpl. The same TreeNode abstraction is used for child and parent relationships, TreeNodeImpl stores a collection of TreeNode children and a parent reference, and the leaf/composite distinction is exposed through `isLeaf()` implemented as `childrenMap.isEmpty()`. No concrete application/domain client usage of TreeNode or TreeNodeImpl was found in the accessible repository, so the verification records that limitation explicitly.

## Event-driven / Spring listener / AOP
Recorded separately from GoF counts because these are architectural/framework mechanisms rather than additional GoF pattern instances.

## Rejected candidates
Rejected/not-confirmed candidates remain in the dataset so that later review can distinguish an investigated candidate from an omitted candidate.

## Re-audit (2026-10-11)
All line citations in `Part1_Findings.md` and `data/patterns.csv` were re-checked against `openwms/org.openwms` at `9d263bf65ec75301e0302539ae7bf581412742b8` and found exact. The copied files under `evidence/source/` are byte-identical to the upstream baseline, and the repository contains 64 Java files as recorded.

Corrections and additions from the re-audit:
- **Observer:** `SimpleEventDispatcher.dispatch` matches listeners by the event's exact runtime class, so subscriptions do not follow the event class hierarchy. Notification is synchronous. No class in the repository implements `EventListener`, so the instance is confirmed at library level without a ConcreteObserver.
- **Composite:** transparent variant with a single implementation class (leaf is a runtime state). `TreeNode` declares no recursive component operation; traversal is left to clients. Classification rests on recursive structure and uniform interface.
- **N03 (AOP):** reclassified from confirmed to partially confirmed. `FireAfterTransactionAspect` is a plain `@Component`; no `@Aspect`, pointcut, advice annotation, XML `aop:` configuration or AspectJ dependency exists in the repository.
- **Singleton rejection:** the candidate beans have public constructors and no static instance or accessor.
