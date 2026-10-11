# CH03 — Persist and publish quiz results

## Requirement

After a student submits answers, persist a result and make it available to both student and instructor result recipients without coupling grading to their concrete notification behavior. Reject non-student submitters and unknown quiz/student IDs.

## Implementation

Added `QuizResult`, its JPA repository, `QuizResultObserver`, `QuizResultPublisher`, and student/instructor observer implementations. `QuizService.grade` saves the result and publishes it to every registered observer. The current concrete recipients log result availability; this is an integration seam, not a claim that email/push notifications have been implemented. The same change fixes the existing authentication-state drift: login calls `AuthService.setUser`, and successful logout calls `clearUser`, so all observers receive the state change.

## Acceptance evidence

`QuizResultPublisherTest` checks that every observer receives the identical result once and that an empty observer list is safe. `QuizServiceIntegrationTest` exercises JPA quiz creation, grading, result persistence and the wired publisher. Angular production build evidence is in `../evidence/frontend_build_output.txt`.

Source patch: `diff.patch`. No verifiable Git commit ID is available for this change; `diff.patch` and the included before/after source files are the available records. The complete tree diff is `../evolved_source.diff`.
