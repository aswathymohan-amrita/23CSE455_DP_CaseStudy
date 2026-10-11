# CH01 — Add quizzes and questions to courses

## Requirement

An instructor needs to associate a quiz with a course they teach and define at least one question. Students and course clients can retrieve a course's quizzes. A quiz must have a nonblank title; each question must have a nonblank prompt and answer and a finite positive point value. An unknown course returns 404, a caller who is not the course instructor receives 403, and invalid quiz input returns 400.

## Implementation

Added `Quiz` and `Question` JPA entities, linked each quiz to one course and each quiz to its questions, and added `POST /api/courses/{courseId}/quizzes` and `GET /api/courses/{courseId}/quizzes`. Public response DTOs omit answer keys. This change adds domain capability and relationships but does not by itself count as a design pattern.

## Acceptance evidence

The final backend integration test creates a course quiz, reloads it through the course query, and uses its persisted question IDs. The quiz response DTO exposes prompts and points but not `correctAnswer`. See `../evidence/backend_test_output.txt`.

Source patch: `diff.patch`. No verifiable Git commit ID is available for this change; `diff.patch` and the included before/after source files are the available records. The complete tree diff is `../evolved_source.diff`.
