# Evolved Part 2 application source snapshot

This folder contains the source files changed for the Part 2 implementation, copied from the `main` branch of the application repository after PR #1 was merged.

- Application repository: https://github.com/nivedita-rmsh/nextjs-blog-cms
- Source merge commit: cd435883322dc29da6943fc871dd40cb1c662299
- Pull request: https://github.com/nivedita-rmsh/nextjs-blog-cms/pull/1

## Changes represented

1. **CH01 — Related article recommendations:** deterministic relevance ranking based on shared tags and category; excludes the current post and posts not approved for public visibility.
2. **CH02 — Content moderation:** moderation-state transitions, admin review queue, and public visibility enforcement.
3. **CH03 — Premium access:** entitlement checks and server-side retrieval of protected premium article content.

## Layout and running

Paths under this directory mirror the source paths in the application repository. This is a snapshot of changed files, not a standalone runnable copy of the full Next.js application. To run the application or tests, clone the application repository and follow its setup instructions.

The focused Vitest test files are included. Their presence does not establish that tests passed. Record actual test, typecheck, lint, build, and database-migration results after running them in the application environment.

The cross-language Part 3 Java/C++ examples are separate from this application snapshot.
