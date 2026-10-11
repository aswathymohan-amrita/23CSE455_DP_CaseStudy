# Part 1 — Baseline source analysis

## Application and baseline

The supplied application is `dinhbachnguyen/E-Learning-App`, an Angular client and Spring Boot REST backend. The baseline is the source archive `A11/E-Learning-App-main.zip`; its SHA-256 is recorded in `evidence/environment.txt`. The archive does not include a Git history or commit identifier, so this report identifies the baseline by archive digest and upstream repository URL rather than inventing a commit. The included `code/` directory is the extracted baseline snapshot.

Scope reviewed: Angular components and services under `src/app`, plus backend controllers, services, entities, repositories, application setup, and the Maven manifest under `elearning-backend`. Generated files, IDE settings, and dependency internals were excluded. The app uses Angular 20, TypeScript, RxJS 7, Java 17, Spring Boot 3.5.6, Spring Data JPA and H2 (versions and limits in `evidence/environment.txt`).

## Architecture

The Angular components call client-side services; the services use `HttpClient` to call Spring REST controllers. Controllers and services operate on JPA repositories and `User`/`Course` entities. The baseline includes course enrollment and authentication, but no quiz domain or quiz API. See `diagrams/architecture.puml`.

## Discovery and verification method

The review scoped inspection to application-owned Angular components/services and Spring controllers/services/entities/repositories. Candidate detection used a manual read of state-holding/delegating/subscribing code plus searches for role-like names and framework annotations; each retained collaboration was confirmed by following declarations, call/subscription sites and data flow in the source. Framework-owned lifecycle behavior and naming-only matches were excluded. This was a manual source review, not a whole-program static analysis. No named reviewer or independent automated claim verifier was recorded.

## Confirmed pattern inventory

One collaboration is confirmed: **Observer — Authentication State Updates** (Behavioral). `AuthService.currentUserSubject` is a concrete subject implemented as an RxJS `BehaviorSubject`; `currentUser$` exposes its observer-facing `Observable` API. The `NavbarComponent` and `HomeComponent` subscribe in `ngOnInit` and assign each emitted user to their `currentUser` state. RxJS supplies the subscription mechanism; there is no application-declared Observer interface, so the mapped observer roles are the callbacks passed to `subscribe`.

The collaboration is structurally confirmed, but its live update flow is incomplete: a search found no baseline caller of `setUser`/`clearUser`. `LoginComponent` writes `currentUser` straight to local storage, and `AuthService.logout()` removes storage without emitting null; `NavbarComponent` clears only its own field in its logout callback. Other subscribers can therefore keep stale state. Change 3 routes login and successful logout through the subject API and adds a separately named quiz-result Observer collaboration.

No additional GoF pattern is counted in the baseline. The controller-service-repository organization is an application/framework architecture, not a specific GoF instance for this inventory. Spring/Angular dependency injection and `@Injectable({providedIn: 'root'})` are framework-managed lifecycle/provisioning, not evidence of a manually implemented Singleton. The list of course lessons does not form a recursive Composite. No swappable baseline scoring policy, explicit Factory collaboration, or quiz-result publisher exists.

## Counts and verification

Baseline totals, using the candidate set actually discussed in this review: **1 confirmed type, 1 confirmed instance, 3 concrete application classes, and 4 unique mapped participant symbols**. The four symbols are `AuthService.currentUserSubject`, `AuthService.currentUser$`, `NavbarComponent.ngOnInit` subscription callback, and `HomeComponent.ngOnInit` subscription callback; RxJS library types are excluded. Four named candidates are rejected/not counted (framework-managed Singleton idiom, MVC/framework architecture, repository/service convention as a GoF instance, flat lesson list as Composite), one is uncertain (Factory), and two named patterns are absent in the baseline (Strategy and quiz-result Observer). These are counts within the documented candidate set and reviewed source scope, not a claim that every possible pattern in the repository was exhaustively enumerated. `evidence/pattern_evidence.md` and the CSV give the source locations and reasons.

| Instance | Type/category | Origin | Mapped participants | Evidence / verification |
|---|---|---|---|---|
| Authentication State Updates | Observer / Behavioral | Existing application code using RxJS | `AuthService.currentUserSubject` (subject); `AuthService.currentUser$` (exposed API); subscription callbacks in `NavbarComponent.ngOnInit` and `HomeComponent.ngOnInit` | `code/src/app/services/auth/auth.service.ts:11-18`; `code/src/app/components/navbar/navbar.component.ts:13-22`; `code/src/app/components/home/home.component.ts:11-19`. Source relationship manually inspected; baseline build/tests were not run; reviewer identity was not recorded. RxJS `BehaviorSubject` supplies replay/current-value behavior. |

The editable architecture diagram is `diagrams/architecture.puml` (rendered form is included with the report). Concise source excerpt from `code/src/app/services/auth/auth.service.ts:11-12`:

```typescript
private currentUserSubject = new BehaviorSubject<any>(null);
currentUser$ = this.currentUserSubject.asObservable();
```

The callbacks in `NavbarComponent:19-22` and `HomeComponent:16-19` subscribe to that API and assign emitted users to local component state. The mapped symbol count includes the subject field, exposed property, and two callbacks, counting callback functions separately from their containing classes. No independent named reviewer or baseline test result is present in the materials.

## Limits

The archive has no original Git metadata. This analysis records source-level evidence but does not claim a full application build or database-backed integration test of the original app. Pattern classification was reviewed manually against the checked-in code; no claim is based solely on previous model output.
