# Part 1 — Pattern Discovery Findings

## Scope and baseline

- Application/ecosystem: OpenWMS.org
- Repository: `org.openwms/org.openwms`
- Baseline commit: `9d263bf65ec75301e0302539ae7bf581412742b8`
- Baseline commit message: `#185 development version 4.1.0-SNAPSHOT`
- Source-level repository scope: root OpenWMS repository, especially the `org.openwms.core.util` Maven module.
- Java source files in the repository at baseline: 64.
- Important scope limitation: the root repository states that business services are developed in their own repositories. Therefore Picking, Inventory, Receiving, Shipping, etc. are part of the wider OpenWMS architecture but are not treated as source-level evidence unless their code is actually present in this repository.

## Architecture finding

OpenWMS describes a distributed microservice architecture. The root repository identifies business services separately and states that Spring Boot microservices are used. RabbitMQ together with Spring Integration is documented as an event broker for asynchronous event and command propagation. The root Maven build contains the `org.openwms.core.util` module.

For this Part 1 baseline, architecture claims are separated from source-level pattern claims. We do not infer a pattern in a missing business service from the architecture documentation alone.

## Method

Candidates were identified from actual Java source at the baseline commit. A candidate is confirmed only when the source demonstrates the relationships and behavior associated with the pattern. Class names, Spring annotations, framework-generated proxies, or an LLM assertion alone are insufficient.

Each candidate is classified as one of:
- GoF design pattern
- Architectural / enterprise pattern
- Framework idiom / mechanism
- Rejected or not confirmed

## Confirmed GoF patterns

### P01 — Observer: Core Event Subscription and Dispatch

**Category:** GoF behavioral pattern.

**Purpose:** decouple event producers from subscribed listeners through explicit subscription, unsubscription, and dispatch.

**Participants:**
- Subject/subscription abstraction: `org.openwms.core.event.EventBroker`
- Subject/dispatcher abstraction: `org.openwms.core.event.EventDispatcher`
- Concrete subject/dispatcher: `org.openwms.core.event.SimpleEventDispatcher`
- Observer abstraction: `org.openwms.core.event.EventListener`
- Event payload/base event: `org.openwms.core.event.RootApplicationEvent`

**Evidence:**
- `EventBroker.java:19-20, 27-30, 32, 35-40, 43-56` explicitly defines subscription/unsubscription of `EventListener` instances to `RootApplicationEvent` types.
- `EventDispatcher.java:19-34` defines dispatch to all subscribed listeners.
- `EventListener.java:19-31` defines the callback invoked when a subscribed event occurs.
- `SimpleEventDispatcher.java:27-38` states that subscribers are stored in an in-memory map and establishes the implementation.
- `SimpleEventDispatcher.java:54-56` registers listeners.
- `SimpleEventDispatcher.java:75-79` removes listeners.
- `SimpleEventDispatcher.java:99-106` obtains the subscribed listeners and invokes `onEvent(event)` for each listener.
- `RootApplicationEvent.java:23-29` establishes the event base type used by the dispatcher/listener collaboration.

**Verification:** Confirmed from source. The collaboration explicitly supports subscribe/unsubscribe and notification. No separate GoF `Subject` class is invented; the subject responsibility is distributed between `EventBroker` (attach/detach), `EventDispatcher` (notify), and `SimpleEventDispatcher` (ConcreteSubject).

**Observations and limitations (added in the 2026-10-11 re-audit):**
- *Exact-type matching.* `SimpleEventDispatcher.java:103` looks up listeners with `subscriptions.get(event.getClass())`. A listener subscribed to `RootApplicationEvent` is therefore not notified of a subclass event such as `UserChangedEvent`; subscriptions do not follow the event class hierarchy.
- *Synchronous notification.* `EventDispatcher.java:28-29` leaves sync/async delivery undefined; `SimpleEventDispatcher.java:27-29` states that subscribers are called sequentially and synchronously. Asynchrony is added only by the separate `NonBlockingEventPublisherImpl` (N01).
- *No ConcreteObserver in scope.* No class in the 64 Java files implements `EventListener`. The repository supplies the Observer infrastructure; concrete observers are expected in the separate service repositories. The instance is therefore confirmed at library level.
- *Publisher is a client, not a participant.* `NonBlockingEventPublisherImpl` calls `EventDispatcher.dispatch`; in GoF terms that makes it a client that triggers notification, which is why it is recorded under N01 rather than counted as an Observer participant.

### P02 — Composite: org.openwms.core.util.TreeNode composite tree

**Category:** GoF structural pattern.

**Purpose:** represent a recursive tree where a node stores children via the same `TreeNode` abstraction and distinguishes leaves from composites by whether the child collection is empty.

**Participants:**
- Component abstraction: `org.openwms.core.util.TreeNode<T>`
- Composite implementation: `org.openwms.core.util.TreeNodeImpl<T>`
- Parent/child containment state: `TreeNode<T> parent`, `Map<Object, TreeNode<T>> childrenMap`
- Leaf/composite behavior: `isLeaf()` implemented as `childrenMap.isEmpty()`

**Evidence:**
- `TreeNode.java:23-28` defines the generic tree-node abstraction.
- `TreeNode.java:45-49` exposes leaf state via `isLeaf()`.
- `TreeNode.java:51-72` exposes child access via `getChildren()` and `getChild()`.
- `TreeNode.java:75-110` provides `addChild`, `removeChild`, `getParent`, and `setParent` using the same `TreeNode` abstraction.
- `TreeNodeImpl.java:29-33` stores `parent` and `childrenMap` and implements `TreeNode`.
- `TreeNodeImpl.java:47-57` implements `addChild` by setting `child.setParent(this)` and storing the child in the map.
- `TreeNodeImpl.java:64-68` implements `removeChild` by removing the child and clearing its parent.
- `TreeNodeImpl.java:83-108` defines `getParent`, `setParent`, `getChildren`, and `isLeaf()` using `childrenMap.isEmpty()`.

**Verification:** Confirmed from source as the GoF Composite collaboration in the repository. The source demonstrates a common component abstraction, recursive child containment, and uniform treatment of child nodes via the same `TreeNode` interface. The implementation does not invent a separate leaf class; instead, it treats leaf state as `childrenMap.isEmpty()`. However, no concrete application/domain client usage of `TreeNode`/`TreeNodeImpl` was found anywhere in the accessible repository; this limitation is recorded explicitly rather than inferred.

**Observations and limitations (added in the 2026-10-11 re-audit):**
- *Transparent Composite, single implementation class.* Child-management operations are declared on the component interface (`TreeNode.java:82-115`), which is the GoF "transparent" variant. There are no separate Leaf and Composite classes: `TreeNodeImpl` plays both roles and "leaf" is a runtime state (`isLeaf()` = `childrenMap.isEmpty()`), not a type.
- *No recursive component operation.* GoF Composite normally has a component operation that a composite forwards to its children. `TreeNode` declares only data access, navigation (`getChildren`, `getChild`, `getParent`) and child management; any traversal is left to the client. The classification therefore rests on recursive structure and uniform interface, not on recursive behaviour. (The Part 3 Composite implementations do include a recursive `traverse` operation.)

## Confirmed non-GoF patterns / mechanisms

### N01 — Event-driven / Publish-Subscribe mechanism

`EventPublisher.java:19-33` describes publication of `RootApplicationEvent` instances to registered `EventListener`s. `NonBlockingEventPublisherImpl.java:22-28, 33-50` provides an asynchronous publisher that delegates to `EventDispatcher.dispatch(event)` and is annotated with Spring `@Async`.

Classification: architectural/eventing mechanism, not an additional GoF Observer instance.

### N02 — Spring Application Event Listener idiom

`LocalServiceInitializer.java:27-33` declares a Spring `ApplicationListener<ContextRefreshedEvent>`. `LocalServiceInitializer.java:50-53` receives the refresh event and publishes a `MergePropertiesEvent` through the Spring `ApplicationContext`.

Classification: framework idiom. It is not counted as a second GoF Observer instance because the subscription/dispatch infrastructure is supplied by Spring.

### N03 — Aspect-Oriented Programming / interceptor mechanism

`FireAfterTransactionAspect.java:30-36` documents the aspect's purpose of firing events after method/transaction completion. Lines 52-66 establish the Spring component and injected `ApplicationContext`; lines 76-85 and 95-107 publish configured events, including asynchronous publication.

Classification: intended AOP advice; not a GoF pattern. **Correction (2026-10-11 re-audit):** the AOP wiring itself is not present in this repository. `FireAfterTransactionAspect` is a plain Spring `@Component` (its imports at lines 18-27 contain no AspectJ types); no class in the repository is annotated `@Aspect`, no `@Around`/`@AfterReturning`/`@Pointcut` advice exists, no XML `aop:` configuration exists, and the `org.openwms.core.util` POM declares no AspectJ dependency. The class provides advice-shaped methods (`fireEvent`, `fireEventAsync`) whose Javadoc describes their use around Spring's transaction advice, but binding them to join points must happen in a consuming service. N03 is therefore recorded as *partially confirmed: advice methods present, interception wiring not in scope*.

## Rejected / not confirmed candidates

| Candidate | Status | Reason |
|---|---|---|
| Singleton | Rejected as GoF evidence | Spring `@Component` or managed-bean behavior alone does not demonstrate intentional GoF Singleton structure. The candidate beans (`SimpleEventDispatcher`, `NonBlockingEventPublisherImpl`, `LocalServiceInitializer`, `FireAfterTransactionAspect`) all have public constructors and no static instance or access method; they are single only because the Spring container scopes them that way. |
| Proxy | Rejected as GoF evidence | Framework-generated proxies/AOP behavior is not counted as an application-level GoF Proxy. |

## Baseline totals

### Strict GoF totals

- Confirmed pattern types: **2** — Observer, Composite
- Confirmed pattern instances: **2** — Core Event Subscription and Dispatch; org.openwms.core.util.TreeNode composite tree
- Concrete participant classes implementing variable roles: **2** — `SimpleEventDispatcher`, `TreeNodeImpl`
- Unique mapped participant symbols: **7** — `EventBroker`, `EventDispatcher`, `SimpleEventDispatcher`, `EventListener`, `RootApplicationEvent`, `TreeNode`, `TreeNodeImpl`
- Rejected/not-confirmed GoF candidates recorded: **2** — Singleton, Proxy

### Broader confirmed non-GoF observations

- Event-driven / Publish-Subscribe mechanism: 1 confirmed architectural observation
- Spring Application Event Listener: 1 confirmed framework idiom
- AOP / transaction-event mechanism: 1 partially confirmed framework mechanism (advice methods present; aspect wiring not in this repository)

These three are deliberately kept separate from the GoF totals.

## Important interpretation

The root OpenWMS repository is not the complete business-service source tree. Therefore the above counts are **repository-scope baseline counts**, not claims that these are the only patterns used by the entire OpenWMS product ecosystem. The business-service repositories must be analyzed separately if their source is available and included in the approved scope.
