# Part 3 — Cross-Language Pattern Implementation

## Pattern selection

The Observer and Composite patterns were selected because Part 1 source inspection of the real OpenWMS CORE repository confirmed Observer participants `EventBroker`, `EventDispatcher`, `EventListener`, `SimpleEventDispatcher`, and `RootApplicationEvent`, and Composite participants `TreeNode` and `TreeNodeImpl`.

Part 3 implements the pattern concepts independently in four languages. These are not copies of the OpenWMS classes and do not modify OpenWMS.

## Common specification

Observer implementations publish Events with string-valued types to three recording observers. The test sequence subscribes all three, publishes `STOCK_LOW`, unsubscribes observer 2, then publishes `STOCK_REPLENISHED`. Event values and the set of recipients are tested.

Composite implementations construct the same location hierarchy:

```text
Warehouse
├── Zone-A
│   ├── A-01
│   └── A-02
└── Zone-B
    └── B-01
```

Preorder recursive traversal must return:

```text
Warehouse, Zone-A, A-01, A-02, Zone-B, B-01
```

Containers and leaves use the same component contract. Containers own child collections and recursively traverse children. Leaves return no children, refuse additions, and cannot remove children.

## Observer

### Java

`ObserverPattern.java` defines `Event`, the `Observer` and `EventSubject` interfaces, `Publisher`, and `RecordingObserver`. The publisher registers interface references and invokes `update` by dynamic dispatch. `ObserverPatternTest.java` runs the three behavior tests using Java assertions implemented as explicit checks.

### Python

`observer.py` defines a frozen dataclass `Event`, abstract `Observer` and `EventSubject` contracts, `Publisher`, and `RecordingObserver`. `Publisher` stores observer objects in a list; Python method dispatch calls each observer's `update`. `test_observer.py` uses standard-library `unittest`.

### JavaScript

`observer.mjs` defines `Event`, contract base classes `Observer` and `EventSubject`, `Publisher`, and `RecordingObserver`. The publisher stores object references in an array and invokes `update` dynamically. `observer.test.mjs` uses Node's built-in strict assertion library and an executable test list.

### C++

`observer.hpp` defines `Event`, abstract `Observer` and `EventSubject` classes, `Publisher`, and `RecordingObserver`. The publisher stores non-owning `Observer*` references and dispatches through virtual `update`. `observer_test.cpp` runs standard `assert` tests. Subscribed observers must outlive their registration because the publisher does not own them.

## Composite

### Java

`CompositePattern.java` defines the shared `Component` interface plus `Container` and `Leaf`. Containers store `Component` references and recursively concatenate child traversals. `getChildren()` returns an immutable snapshot. `CompositePatternTest.java` tests construction, add/remove, leaf constraints, and traversal.

### Python

`composite.py` defines an abstract `Component`, `Container`, and `Leaf`. The container stores component references and returns an immutable tuple snapshot of children. `test_composite.py` uses standard-library `unittest`.

### JavaScript

`composite.mjs` defines a common `Component` contract class plus `Container` and `Leaf`. Containers own an array of component references and return a shallow snapshot from `getChildren()`. `composite.test.mjs` uses Node's built-in strict assertions.

### C++

`composite.hpp` defines an abstract `Component`, a `Container`, and a `Leaf`. Containers own children through `std::shared_ptr<Component>` and return a vector copy from `getChildren()`. The virtual `traverse()` method recursively builds the preorder result. `composite_test.cpp` runs standard `assert` tests.

## Test commands

All commands below were executed from the named pattern/language directory. Java class files and C++ executables were written under `$env:TEMP\part3-metrics-audit`, outside the project. Python's `-B` disables bytecode-cache creation.

| Pattern/language | Test command |
|------------------|--------------|
| Observer / Java | `javac -d $env:TEMP\part3-metrics-audit\java-observer ObserverPattern.java ObserverPatternTest.java; java -cp $env:TEMP\part3-metrics-audit\java-observer ObserverPatternTest` |
| Observer / Python | `"python" -B -m unittest -v test_observer.py` |
| Observer / JavaScript | `node observer.test.mjs` |
| Observer / C++ | `g++ -std=c++20 -Wall -Wextra -Werror -pedantic observer_test.cpp -o $env:TEMP\part3-metrics-audit\observer-cpp.exe; & $env:TEMP\part3-metrics-audit\observer-cpp.exe` |
| Composite / Java | `javac -d $env:TEMP\part3-metrics-audit\java-composite CompositePattern.java CompositePatternTest.java; java -cp $env:TEMP\part3-metrics-audit\java-composite CompositePatternTest` |
| Composite / Python | `"python" -B -m unittest -v test_composite.py` |
| Composite / JavaScript | `node composite.test.mjs` |
| Composite / C++ | `g++ -std=c++20 -Wall -Wextra -Werror -pedantic composite_test.cpp -o $env:TEMP\part3-metrics-audit\composite-cpp.exe; & $env:TEMP\part3-metrics-audit\composite-cpp.exe` |

The observed toolchains were OpenJDK 25.0.4.1 (Eclipse Temurin), Python 3.13.15, Node.js v24.21.0, and g++ 16.2.0 using C++20.

## Test results

| Pattern | Java | Python | JavaScript | C++ |
|---------|------|--------|------------|-----|
| Observer | 3/3 passed | 3/3 passed | 3/3 passed | 3/3 passed |
| Composite | 4/4 passed | 4/4 passed | 4/4 passed | 4/4 passed |

These results came from the executions above: the Java/C++ harnesses reported their pass counts, Python `unittest` reported 3 and 4 successful cases, and the Node harnesses reported 3 and 4 passing assertions. Total: 28/28 checks across all languages and patterns, with no failures. Java and C++ use executable assertion harnesses; Python uses `unittest`; JavaScript uses Node's built-in `node:assert/strict`.

## Metrics

Counts were recalculated from the actual two source files in every pattern/language directory: one implementation source and one test source. LOC is physical lines including blank lines; generated files, this report, and CSV files are excluded. `Types` counts production participant types (including Event and abstract contracts, excluding test-harness types); the C++ Observer Event is a struct and is included in its type count.

### Static metrics

Lizard 1.24.1 analyzed both implementation and test files in each directory. Maximum cyclomatic complexity and function names below are the maximum across those analyzed files; tied functions are all listed. All eight cells were parsed by the same analyzer, so no language-specific complexity tool substitution was needed.

| Pattern | Language | Implementation LOC | Test LOC | Total LOC | Source files | Types | Max cyclomatic complexity | Function(s) at max |
|---------|----------|--------------------:|---------:|----------:|-------------:|------:|-------------------------:|--------------------|
| Observer | Java | 65 | 70 | 135 | 2 | 5 | 2 | `Publisher.publish`, `Publisher.subscribe`, `ObserverPatternTest.check` |
| Observer | Python | 52 | 37 | 89 | 2 | 5 | 3 | `setUp`, `test_event_values_and_object_are_preserved` |
| Observer | JavaScript | 54 | 43 | 97 | 2 | 5 | 2 | `Publisher.subscribe`, `Publisher.publish` |
| Observer | C++ | 55 | 61 | 116 | 2 | 5 | 2 | `Publisher::publish`, `Publisher::subscribe`, `test_event_values_are_preserved` |
| Composite | Java | 89 | 63 | 152 | 2 | 3 | 2 | `Container.traverse`, `CompositePatternTest.check`, `CompositePatternTest.testLeafRejectsChildren` |
| Composite | Python | 71 | 48 | 119 | 2 | 3 | 2 | `Container.remove_child`, `Container.traverse` |
| Composite | JavaScript | 81 | 47 | 128 | 2 | 3 | 2 | `Container.removeChild` |
| Composite | C++ | 85 | 62 | 147 | 2 | 3 | 2 | `Container::removeChild`, `Container::traverse`, `test_leaf_rejects_children` |

These are analyzer-reported values, not manually inferred complexity estimates. The expanded machine-readable table is [`metrics/cross_language.csv`](metrics/cross_language.csv). The existing structural counts remain in [`metrics/pattern_metrics.csv`](metrics/pattern_metrics.csv).

### Dynamic metrics

For each harness, the already-compiled Java classes and C++ executables were invoked as separate processes; compilation was not timed. Python and JavaScript were likewise invoked as separate processes. The same PowerShell `System.Diagnostics.Stopwatch` process-launch-to-exit measurement was used for every language. Each harness received one untimed warm-up execution followed by 30 measured executions; the reported statistic is the median of the 30 elapsed process times. Each execution reran the corresponding complete tests. Units are microseconds.

| Pattern | Language | Median process time (µs) | Timed runs | Warm-up runs |
|---------|----------|-------------------------:|-----------:|-------------:|
| Observer | Java | 175141.500 | 30 | 1 |
| Observer | Python | 279278.150 | 30 | 1 |
| Observer | JavaScript | 128565.450 | 30 | 1 |
| Observer | C++ | 33064.200 | 30 | 1 |
| Composite | Java | 153990.750 | 30 | 1 |
| Composite | Python | 264598.450 | 30 | 1 |
| Composite | JavaScript | 130189.700 | 30 | 1 |
| Composite | C++ | 33436.600 | 30 | 1 |

### Complexity

Cyclomatic complexity was measured with the same Lizard 1.24.1 installation for Java, Python, JavaScript, and C++. Lizard was installed in an isolated temporary virtual environment, not in the project. The analyzer was run on each of the eight pattern/language directories and parsed the implementation plus test file. The table reports the largest function-level CCN in that directory and all tied function names. Lizard successfully returned function-level results for all four languages; there were no tool-limitation omissions. These values describe the functions as parsed by Lizard and do not claim equivalent parser semantics across languages.

The algorithmic costs are separate from cyclomatic complexity: subscription membership/removal is linear in subscriber count, publication is linear in subscribed observers, Composite traversal is O(V + E), and child-list add/remove are linear in child count for these collection implementations.

## Structural comparison

Observer structure is the same in every implementation: one publisher references the observer abstraction and sends an Event through the observer operation; each recording observer retains its event sequence. All implement the three-subscription scenario without framework event facilities.

Composite structure is also equivalent: one component abstraction, one container holding components, and one leaf implementing the same traversal interface. Both concrete node types have inheritance depth one from the component abstraction. Recursive traversal is preorder in every language.

## Abstraction comparison

- **Java:** Explicit interfaces separate `Observer`, `EventSubject`, and `Component` contracts from their implementations.
- **Python:** ABCs make the contracts explicit while runtime object references and typing annotations describe relationships.
- **JavaScript:** Base classes express expected operations by throwing until overridden; the language does not provide a built-in interface type.
- **C++:** Pure virtual classes express contracts with compile-time checking and virtual dispatch.

## Coupling comparison

For Observer, the publisher depends on the observer contract rather than the concrete recording observer. Observer implementations depend on the Event value. Registration stores references in a list/vector/array; unsubscribe removes the reference and publish dispatches the event. Java/Python/C++ declare these relationships in signatures; JavaScript expresses them through method calls.

For Composite, containers hold and traverse children using the common component abstraction. Leaves and containers both conform to that abstraction, so clients can call `getName`, child operations, `getChildren`, and `traverse` without branching on concrete type. Leaves reject addition, return no children, and return their own name during traversal.

## Language-specific observations

1. **Type system:** Java and C++ statically declare contracts; Python ABCs add runtime-enforced abstract operations; JavaScript uses class conventions and runtime method checks.
2. **Boilerplate:** Explicit interfaces and method signatures require more code in Java/C++; Python's syntax is shorter. Actual LOC above includes the test harnesses and is not normalized for formatting.
3. **Runtime dispatch:** Java virtual/interface calls, Python method dispatch, JavaScript method dispatch, and C++ virtual calls all reach the same observer/component operations.
4. **Ownership:** Java, Python, and JavaScript use managed object references. C++ Composite uses `shared_ptr` for child ownership. C++ Observer registrations are non-owning raw pointers and require observers to outlive their subscriptions.
5. **Collection behavior:** Implementations use standard lists, tuples/snapshots, arrays, and vectors; no framework or external dependency is used.
6. **Complexity:** Lizard's maximum function CCN is low in all eight implementations, but these parser-based values are analyzer-specific and are not universal measures of design quality. No language is claimed to be universally better; measured LOC reflects syntax and API style as well as the same specification.

## Traceability to OpenWMS

The Observer concept was selected based on confirmed OpenWMS CORE source participants `EventBroker`, `EventDispatcher`, `EventListener`, `SimpleEventDispatcher`, and `RootApplicationEvent`. The Composite concept was selected based on confirmed `TreeNode` and `TreeNodeImpl`.

The eight implementations here are independent reference implementations of those pattern concepts. They are not copied from or integrated with those classes, and they do not change CORE, CH01, CH02, or any canonical OpenWMS source.

## Limitations

- These are reference implementations for a comparative case study, not production-ready event or warehouse-location subsystems.
- They do not modify OpenWMS source.
- The implementations are independent reference implementations, not OpenWMS modifications.
- LOC is physical LOC, measured from the actual implementation and test files using the definitions above.
- The complexity figures depend on Lizard 1.24.1's language parsers and function analysis.
- These tiny programs' observed process times are dominated by process/runtime startup overhead; they are not general language-performance benchmarks, and no language is claimed to be universally faster.
- Framework-specific behavior was avoided; Java uses only the JDK, Python uses `unittest`, JavaScript uses Node's built-in assertion module, and C++ uses the standard library and `assert`.
- The Observer test harnesses are executable checks rather than a common cross-language test framework, so framework reporting formats differ while scenarios and assertions remain equivalent.

## Independent re-run (2026-10-11)

All eight harnesses were re-run on a second machine (Linux) with OpenJDK 21.0.12.1, Python 3.13.16, Node.js v22.22.0 and g++ 13.3.0 (`-std=c++20 -Wall -Wextra -Werror -pedantic`). The results were again Observer 3/3 and Composite 4/4 in every language, for 28/28 in total. Physical LOC for all sixteen files and Lizard 1.24.1 maximum CCN for all eight directories were recomputed and match the tables above exactly. Timing was not re-measured.
