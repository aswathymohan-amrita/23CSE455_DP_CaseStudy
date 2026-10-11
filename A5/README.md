# Team A5 — Design Pattern Identification and Evolution in a Laravel Healthcare Application

**Course:** 23CSE455 Design Patterns  
**Study:** Source-based architecture analysis, change-impact assessment, design-pattern evolution, cross-language comparison and validation  
**Original application:** [esteham/hospital-management](https://github.com/esteham/hospital-management)  
**Fixed baseline commit:** `1e7420e431771e3f5eec470d8a005e8255fa5fe8`

## 1. Team and study overview

| Student | Roll number | Proposed two-pattern extension |
| --- | --- | --- |
| Nemali Ashrith Reddy | AM.AL.U4AID23014 | Facade, Repository |
| Akshay Reddy Velugati | AM.AL.U4AID23062 | Adapter, Strategy |
| B. Pravallika | AM.SC.U4CSE23212 | Proxy, Observer |
| Daripineni Manogna | AM.SC.U4CSE23022 | Factory Method, Decorator |

The table identifies the intended division of the eight-pattern extension, **not independent verification of each student's individual authorship**. Earlier contributions to the three original assignment parts are documented in the report.

This project examines an existing Laravel 12/PHP 8.2+ hospital-management system. The application uses Vue 3/Inertia for its interface and Eloquent for persistence. The study traces patient/doctor relationships, appointment bookings, diagnostic bookings, prescriptions and PDF/mail flows, and payment-related fields. It then evaluates how the architecture could evolve when integrating new laboratory, billing and patient-data providers.

**Evidence boundary:** baseline findings come from the inspected commit and saved excerpts under `data/code/`. The eight-pattern implementations, external-provider adapters and Laravel overlay are **new case-study work**, not observed patterns in that baseline. No live medical, laboratory or payment credentials or production patient records are used.

## 2. Deliverables and navigation

| Deliverable | Path | Contents |
| --- | --- | --- |
| Compiled report | [A5_Report.pdf](A5_Report.pdf) | Formal report with findings, diagrams, results, allocation and conclusion |
| Report source | [A5_Report.tex](A5_Report.tex) | Editable LaTeX; compiled by CI |
| Baseline inspection | [Part1/](Part1/) | Source evidence, pattern inventory/counts, current architecture and LLM verification |
| Three change scenarios | [Part2/changes/](Part2/changes/) | Requirements, change notes and test-result evidence for CH01–CH03 |
| PHP service prototypes | [Part2/code/](Part2/code/) | Laboratory, billing and EHR service roles |
| Eight-pattern PHP implementation | [Part2/eight_patterns/](Part2/eight_patterns/) | Pattern contracts, concrete classes, deterministic contract tests and inventory |
| Laravel integration overlay | [laravel_integration/](laravel_integration/) | Install script, controller, service bindings, protected routes, configuration and HTTP-fake tests |
| Original Adapter/Strategy demos | [Part3/adapter/](Part3/adapter/) and [Part3/strategy/](Part3/strategy/) | Earlier four-language exercises and captured outputs |
| Eight-pattern language matrix | [Part3/eight_patterns/](Part3/eight_patterns/) | 32 standalone programs, execution commands, benchmark and measurements |
| Consolidated evidence | [data/](data/) | Source excerpts, tabular datasets and recorded test outputs |
| Validation workflow | [../.github/workflows/a5-validate.yml](../.github/workflows/a5-validate.yml) | PHP, language, upstream Laravel, benchmark and PDF checks |

## 3. Part 1 — Existing system and pattern identification

The application routes HTTP requests to Laravel controllers, which validate inputs and use Eloquent models to persist domain entities. Its inspected functionality includes appointments, diagnostic services/bookings, patient and doctor data, prescriptions and PDF/email handling.

The **observed baseline** includes Eloquent's **Active Record** style and **Laravel framework Facades**. The inspected modules did not establish a custom Adapter, Strategy, Proxy, Repository or Observer implementation. An existing class named `DiagnosticService` is a catalogue model, **not** the newly proposed external laboratory integration service.

Supporting evidence: [Part1/patterns.csv](Part1/patterns.csv), [Part1/Pattern_count.csv](Part1/Pattern_count.csv), [current architecture diagram](Part1/pattern_architecture/current_architecture.pdf) and [inspected source excerpts](data/code/). Baseline counts must not be inflated by including newly proposed patterns.

## 4. Part 2 — Change-impact and design evolution

| Change | Existing behavior / evidence | Proposed boundary | Status |
| --- | --- | --- | --- |
| **CH01: external laboratory** | Diagnostic booking persists a `BookingDiagnostic` row; an external vendor integration is not established | `LabGateway` with an HTTP adapter and explicit payload translation | PHP prototype plus installable Laravel overlay, tested with fake HTTP responses |
| **CH02: billing provider** | Booking records store payment method/status; this does not prove a live payment gateway | `BillingGateway` / interchangeable provider Strategy, transaction reference and idempotency header | PHP prototype plus Laravel overlay; real charge/reconciliation not verified |
| **CH03: patient-data service** | Application reads local patient-related models and prescriptions | `PatientGateway` with a FHIR-style Adapter | PHP prototype plus Laravel overlay; real EHR consent/security not verified |

The architecture evolution and UML artifacts are in [Part2/diagrams/](Part2/diagrams/). The initial service design and the separate eight-pattern exercise are documented in [Part2/code/](Part2/code/) and [Part2/eight_patterns/](Part2/eight_patterns/).

### Eight proposed pattern collaborations

| Pattern | Representative healthcare use case | Design intent |
| --- | --- | --- |
| Facade | Appointment booking and notification | Present one simple entry point for coordinated operations |
| Repository | Patient persistence | Decouple client logic from storage details |
| Adapter | External laboratory order payload | Translate incompatible vendor interfaces |
| Strategy | Billing provider selection | Substitute payment behavior behind a stable contract |
| Proxy | Patient-data cache | Control and cache access to a wrapped source |
| Observer | Clinical event notifications | Decouple event publication from subscribers |
| Factory Method | Medical-record export | Delegate exporter creation to specialized factories |
| Decorator | Medical-record read audit | Add audit behavior without changing the reader contract |

These examples use synthetic inputs and in-memory or simulated collaborators. The Facade here is a **new application-level design**, distinct from Laravel's pre-existing framework Facades.

## 5. Part 3 — Cross-language implementation and measurements

Each of the eight patterns is demonstrated independently in **Java, Python, JavaScript and C++** (32 source files). These reduced examples illustrate participant roles and substitution; they are not Laravel integrations. The earlier detailed Adapter and Strategy exercises remain separately available under `Part3/adapter/` and `Part3/strategy/`.

The complete source-path/command matrix is [Part3/eight_patterns/cross_language.csv](Part3/eight_patterns/cross_language.csv). The reproducible benchmark is [benchmark.py](Part3/eight_patterns/benchmark.py), and [measured_results.csv](Part3/eight_patterns/measured_results.csv) records measured source LOC, five raw process-level runs and median execution time per implementation. **Process startup is included; compilation is excluded. Maximum function cyclomatic complexity is measured with Lizard 1.21.0**, and results are machine-dependent rather than cross-machine performance rankings.

## 6. How to run and reproduce

### Requirements

- PHP 8.2+ for the standalone PHP contracts
- Python 3, Node.js, Java JDK and a C++17 compiler for the cross-language programs
- Composer and a Laravel 12-compatible PHP environment for the upstream overlay tests
- LaTeX packages (`pdflatex`, including `texlive-latex-extra`) for the report

From the `A5/` directory:

```sh
# Standalone PHP pattern contracts
php Part2/eight_patterns/test.php

# Part 2 integration contract checks
php Part2/tests/integration_contracts.php

# All 32 programs, raw process timings and source LOC
python3 -m pip install lizard==1.21.0
python3 Part3/eight_patterns/benchmark.py
python3 Part3/eight_patterns/audit_faculty_dataset.py

# Compile the report (twice for references)
pdflatex -interaction=nonstopmode -halt-on-error A5_Report.tex
pdflatex -interaction=nonstopmode -halt-on-error A5_Report.tex
```

To test the **Laravel overlay against the actual inspected upstream**:

```sh
git clone https://github.com/esteham/hospital-management.git hospital-management
cd hospital-management
git checkout 1e7420e431771e3f5eec470d8a005e8255fa5fe8
cd ..
python3 /path/to/A5/laravel_integration/install.py hospital-management
cd hospital-management
composer install
cp .env.example .env
php artisan key:generate
php artisan test --filter=CaseStudyIntegrationsTest
php artisan route:list --path=case-study
```

The installer adds a controller, three service contracts/adapters, a provider, config, protected routes and Laravel feature tests. It patches the **target checkout**'s provider registration and web routes. It does **not** rewrite the original booking controllers or deploy to a running server. The tests use `Http::fake()`, not real providers. The default local endpoint URLs are deliberately nonproduction placeholders. For implementation details, see [laravel_integration/README.md](laravel_integration/README.md).

### Automated verification

The [A5 validation workflow](../.github/workflows/a5-validate.yml) executes PHP contracts, all 32 language demonstrations, process benchmarks, overlay installation into the pinned upstream source, Laravel HTTP-fake tests and LaTeX compilation. The [successful validation run](https://github.com/Rashrith7/23CSE455_DP_CaseStudy/actions/runs/38131329143) documents those checks. CI commits the generated PDF and measurement CSV back to the study branch; inspect the workflow when repeating a build.

## 7. Report structure

The report follows the study in order: application selection and architecture; **Part 1 baseline evidence**; **Part 2 three change scenarios and refactoring**; **Part 3 language implementations and eight-pattern extension**; LLM evidence and team contributions; **conclusion and references**. The eight-pattern section is deliberately **before** the conclusion, not appended after the bibliography. The PDF and LaTeX are maintained together.

## 8. Data provenance, limitations and responsible use

- The baseline is fixed to one upstream commit. New code must not be described as existing in the original system.
- The Laravel overlay is installed and tested in CI, but its three endpoints are additional routes; the original business flows remain unchanged.
- Laboratory, billing and FHIR responses are mocked. No real vendor credentials, live payments or patient records are involved.
- A production integration would require patient consent, authorization and auditing, secret management, gateway signature checks, retries, idempotency, reconciliation, failure handling and deployment review.
- Measurements are **process-level** and not steady-state throughput. Source LOC is recorded; cyclomatic complexity remains unmeasured.
- The proposed two-pattern-per-member allocation is a planning/documentation record, not independently verified authorship.
- LLM involvement, verification notes and source references are recorded in the corresponding Part 1–3 evidence files. Refer to the report for the full methodology and citations.

## 9. References

1. [esteham/hospital-management](https://github.com/esteham/hospital-management), inspected at commit `1e7420e431771e3f5eec470d8a005e8255fa5fe8`.
2. Gamma, Helm, Johnson and Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software* (1994).
3. [Laravel documentation](https://laravel.com/docs/12.x).



