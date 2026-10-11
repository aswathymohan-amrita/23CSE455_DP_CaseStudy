# Shared specification: quiz scoring and result notification

Selected patterns: Strategy and Observer.

Fixture questions: (Q1, 10 points, correct A), (Q2, 5 points, correct B), (Q3, 5 points, correct A). Submitted answers: Q1=A, Q2=B, Q3=C.

Scoring rules:
- StandardStrategy: correct answers earn full points; wrong/unanswered answers earn zero. Expected score: 15.
- NegativeMarkingStrategy: correct answers earn full points; answered wrong answers subtract max(1, floor(points/2)); unanswered answers do not change score; final score is floored at zero. Expected score: 13.
- Empty answers yield 0 for both strategies. Answers keyed by an unknown question ID are ignored (the score remains 15 for the fixture plus `{999: A}`).

Observer rule: publish result {quizId:101, studentId:7, score:15}; StudentResultObserver and InstructorResultObserver each receive exactly one event and produce respectively `student:7 quiz:101 score:15` and `quiz:101 score:15`.

Test runner must make assertions and exit non-zero on failure. Six assertions cover standard score, negative score, empty answers, unknown answer ID, and one exact notification per observer. Output: `PASS 6/6`.
