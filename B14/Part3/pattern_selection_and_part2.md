# Pattern selection and Part 2 notes

## Why these two patterns?

Part 1 confirmed Strategy in the AI provider streaming code and Observer in the auth subscription code. Both have roles that we can point to in the original app. RBAC remains in the Part 1 count, but the team chose Strategy and Observer for the two-pattern Part 3 comparison.

## Part 2 feature changes

The cumulative application work uses these labels:

- **CH01, related articles:** ranks published, approved posts using shared tags and category. It adds one ranking function, not a family of interchangeable strategies.
- **CH02, content moderation:** adds a review step before publication. It adds access and status rules, but no confirmed GoF State pattern.
- **CH03, premium content:** stores the full body separately and checks entitlement before reading it. This extends access control, not the selected Strategy or Observer collaboration.

The existing LLM streaming Strategy and auth Observer remain in the evolved app. The feature implementation lives in the separate application branch documented in `../Part2/` and the team report. The copy under `../code/` is the original baseline, not the cumulative feature branch.

## Separate refactoring experiments

Part 2 also records three small refactoring experiments on separate branches: provider inference in `generateBlogPost()`, publication title/content validation helpers, and a shared generated-post JSON parser. These are different from feature changes CH01 to CH03. The baseline `../code/features/ai-assistant/llmService.ts` does not contain the provider-inference or JSON-parser helpers. These experiments do not establish a new confirmed pattern instance in Part 3.

## Original source mapping

- Strategy: `../Part1/patterns.csv`; `../code/features/ai-assistant/llmService.ts` at baseline commit `90ec6565877053ee0e93e9f09dcc7c7213aa4832`.
- Observer: `../Part1/patterns.csv`; `../code/features/auth/context/AuthProvider.tsx` and `AuthContext.tsx` at the same baseline.
