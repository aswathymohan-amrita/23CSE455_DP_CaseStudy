# Pattern evidence and rejected candidates

## Confirmed: Observer — Authentication State Updates

| Role | Actual participant | Evidence |
|---|---|---|
| Concrete subject | `AuthService.currentUserSubject: BehaviorSubject<any>` | `code/src/app/services/auth/auth.service.ts:11,21-29` |
| Subject-facing API | `AuthService.currentUser$` | `.../auth.service.ts:12` |
| Observer role | callback supplied to RxJS `Observable.subscribe` | `.../navbar.component.ts:19-22`; `.../home.component.ts:16-19` |
| Concrete observers | `NavbarComponent`; `HomeComponent` | same callback sites, each assigns emitted user to component state |

The subject emits in `setUser` and `clearUser`; its constructor also publishes persisted state on startup. Consumers subscribe to `currentUser$`. This is behavioral broadcast of state changes and decouples the subject from its components. A repository search found no other baseline call sites for `setUser` or `clearUser`: `LoginComponent` writes local storage directly and successful logout removes storage without calling `clearUser`. The Observer structure is present, but the live authentication update flow is only partially connected; the collaboration should be described with that limitation, not as working end-to-end state propagation.

## Rejected or uncertain candidates

| Candidate | Decision | Reason |
|---|---|---|
| Singleton (`AuthService`, `CourseService`) | Not counted; framework idiom | Angular root provisioning controls service lifetime; there is no explicit singleton construction or access protocol authored by this application. |
| MVC | Not counted as a GoF collaboration | Spring MVC and Angular provide architectural roles, but the assignment requests specific pattern collaborations and the current source does not implement a standalone MVC pattern instance. |
| Repository / Service | Not counted as GoF patterns | These are framework/application layering conventions in this project, not one of the requested GoF collaborations. |
| Composite (`Course.lessons`) | Rejected | `List<String>` is flat data; no common component contract, recursive composition, or uniform leaf/composite operation exists. |
| Strategy | Not present in baseline | No interchangeable scoring or other policy interface and concrete alternatives exist. |
| Factory | Not confirmed | No application function/class creates a family of interchangeable products behind a common product contract. Framework constructors/DI are outside this claim. |
| Quiz-result Observer | Not present | The baseline contains no quiz, result, publisher, or result recipients. |

## Source archive identity

Baseline source is the extracted archive in `Part1/code/`. Archive URL: `https://github.com/dinhbachnguyen/E-Learning-App`. Exact source archive: `A11/E-Learning-App-main.zip`; digest and environment notes are in `environment.txt`.
