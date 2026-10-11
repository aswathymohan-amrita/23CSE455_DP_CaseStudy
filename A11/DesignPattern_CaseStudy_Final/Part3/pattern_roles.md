# Participant mapping by language

## Strategy — Quiz scoring policy

| Role | Java | Python | JavaScript | C++ |
|---|---|---|---|---|
| Strategy contract | `ScoringStrategy` interface | `ScoringStrategy(ABC)` | `ScoringStrategy` base class | `ScoringStrategy` pure virtual class |
| Concrete strategy A | `StandardScoringStrategy` | `StandardScoringStrategy` | `StandardScoringStrategy` | `StandardScoringStrategy` |
| Concrete strategy B | `NegativeMarkingStrategy` | `NegativeMarkingStrategy` | `NegativeMarkingStrategy` | `NegativeMarkingStrategy` |
| Context | `QuizGrader` | `QuizGrader` | `QuizGrader` | `QuizGrader` |
| Input model | `Question` record | `Question` dataclass | `Question` class | `Question` struct |

## Observer — Quiz result notification

| Role | Java | Python | JavaScript | C++ |
|---|---|---|---|---|
| Subject | `QuizResultPublisher` | `QuizResultPublisher` | `QuizResultPublisher` | `QuizResultPublisher` |
| Observer contract | `QuizResultObserver` interface | `QuizResultObserver(ABC)` | `QuizResultObserver` base class | `QuizResultObserver` pure virtual class |
| Concrete observer A | `StudentResultObserver` | `StudentResultObserver` | `StudentResultObserver` | `StudentResultObserver` |
| Concrete observer B | `InstructorResultObserver` | `InstructorResultObserver` | `InstructorResultObserver` | `InstructorResultObserver` |
| Event payload | `QuizResult` record | `QuizResult` dataclass | `QuizResult` class | `QuizResult` struct |
