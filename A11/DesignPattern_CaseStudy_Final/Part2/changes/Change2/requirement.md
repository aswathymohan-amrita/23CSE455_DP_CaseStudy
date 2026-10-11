# CH02 — Make quiz scoring selectable

## Requirement

Support standard scoring and negative marking through the same grading flow. Standard scoring awards points for correct answers and zero for wrong, missing or unknown-question answers. Negative marking subtracts half of a question's points for an answered incorrect response, leaves unanswered questions neutral, and clamps the total at zero. The selected rule must not be hard-coded into quiz orchestration.

## Implementation

Added `ScoringStrategy`, `StandardScoringStrategy`, and `NegativeMarkingScoringStrategy`; `QuizService` chooses the configured implementation based on the grade request. The same question/answer map feeds both implementations. Two concrete policy classes form one Strategy collaboration, not two instances.

## Acceptance evidence

`ScoringStrategyTest` covers correct, wrong, unanswered, unknown and all-wrong inputs. The integrated sample quiz also checks a 7.5 negative-marking score. See `../evidence/backend_test_output.txt`.

Source patch: `diff.patch`. No verifiable Git commit ID is available for this change; `diff.patch` and the included before/after source files are the available records. The complete tree diff is `../evolved_source.diff`.
