# Part 3: Cross-language analysis and quality audit

## Pattern selection and roles

**Strategy (behavioural):** `ScoringStrategy` is the strategy contract; `StandardScoringStrategy` and `NegativeMarkingStrategy` are concrete strategies; `QuizGrader` is the context and delegates calculation. The input model is `Question`.

**Observer (behavioural):** `QuizResultPublisher` is the subject; `QuizResultObserver` is the observer contract; `StudentResultObserver` and `InstructorResultObserver` are concrete observers; `QuizResult` is the event payload.

## Shared behaviour

See `spec.md`. All implementations receive the same three questions and answer map, return standard score 15 and negative-marking score 13, return 0 for empty answers, ignore answers keyed to unknown question IDs, and deliver exactly one result event to each registered observer. Every test runner exits non-zero on assertion failure and prints `PASS 6/6` only on success.

## Application architecture and request flow

Student opens a course → Angular course detail requests course quizzes → student opens a quiz → Angular Quiz API Service sends answers to `QuizController` → `QuizService` validates and coordinates → `QuizGrader` delegates to the configured Strategy → result is persisted → `QuizResultPublisher` notifies registered observers. Instructor quiz creation/question management is shown at the architecture boundary, but the cross-language snippets intentionally isolate the two pattern collaborations rather than reproduce the entire full-stack application.

Editable sources are `diagrams/architecture.puml`, `diagrams/strategy_observer.puml`, and the Graphviz `.dot` files. Rendered architecture/class diagrams are PNG/SVG files.

## Three evolution changes

1. **CH01 — Course/Quiz association.** Add a one-to-many `Course.quizzes` relationship, so quizzes become discoverable through a course. Existing authentication Observer is preserved. Exact diff between included example snapshots: `changes/CH01/CH01.diff`.
2. **CH02 — scoring policy extraction.** Replace inline score calculation with `ScoringStrategy`; introduce standard and negative-marking strategies. Strategy is newly introduced, not merely renamed. Exact diff between included example snapshots: `changes/CH02/CH02.diff`.
3. **CH03 — result notification.** Replace hard-coded calls to student and instructor notifications with publication to `QuizResultPublisher`. Observer is newly introduced for quiz result events. Exact diff between included example snapshots: `changes/CH03/CH03.diff`.

**Evidence limitation:** these are exact diffs between included illustrative before/after snapshots, but not Git-derived diffs against a verified baseline commit. These are illustrative snapshots only; no exact repository commit history was supplied.

## Language comparison

- **Java:** explicit interfaces and compiler-checked contracts. Strategy and Observer roles are visible in declarations; more boilerplate, static checks catch incompatible collaborators earlier.
- **Python:** `ABC` and `@abstractmethod` make intent explicit, while duck typing still permits compatible objects without inheritance. Concise implementation, with contract failures generally found at runtime.
- **JavaScript:** class syntax supports familiar role names, but the language does not enforce interfaces. A compatible object can satisfy the method contract structurally; flexible but easier to break accidentally.
- **C++:** pure virtual base classes provide explicit polymorphic contracts. Native execution is fast in this small process test, but Observer stores non-owning pointers; subscriber lifetime must be managed by the caller.

## Static/dynamic metric interpretation

`cross_language.csv` contains eight rows (two patterns × four languages), source LOC, maximum function CC, actual test result, compiler/runtime, command and median process time. LOC currently counts nonblank/non-comment physical lines in each production source file, and each source file contains both pattern implementations. Thus LOC is repeated across the two rows for a language and **must not be interpreted as pattern-only LOC**. Some source is compactly formatted; a stronger LOC comparison should reformat each language idiomatically and report separate files per pattern. The complexity values are manually checked using CC = 1 + decision points (`if`, `for`, `while`, `case`, `catch`, `&&`, `||`) for the most complex method in that pattern. They are useful as a transparent course-level estimate, not a substitute for a named analyzer such as Lizard.

Timing is whole-process wall time including interpreter/JVM startup, input construction, pattern execution and output capture; compilation is excluded. With a tiny fixture, startup dominates. Do not conclude that C++ Strategy/Observer dispatch is intrinsically 35–500× faster. A stronger experiment would warm a long-running process and time millions of operations separately from startup.

## Audit of the earlier draft work

The earlier draft had several items that should not be submitted unchanged:

1. Some source LOC/CC values were manually entered and not traceable to a named counting script. This version records its rule and marks the limitations.
2. Previous timing values were from a different run/environment and should not be mixed with this run. This version uses fresh five-run medians and stores raw samples.
3. The earlier `llm.csv` claimed a model/date string that was not independently substantiated. The available package does not establish the displayed model, access tier, or date for this artifact. `llm.csv` now records those fields as unavailable and distinguishes the prompt artifact from raw output.
4. Earlier diffs were proposed snippets rather than guaranteed Git-exact diffs. This report labels that fact explicitly and requires real commit-derived diffs before submission.
5. Earlier test results were repeated as if they demonstrated the integrated application. They only validated isolated cross-language examples. This version distinguishes the isolated Part 3 tests from full Angular/Spring integration tests.
6. The old architecture and role mappings needed to separate existing authentication Observer from the new quiz-result Observer. This report does so.
