# Part 2 — Evidence of evolution and limitations

## Reproducible source versions

- **Before:** [esteham/hospital-management at 1e7420e431771e3f5eec470d8a005e8255fa5fe8](https://github.com/esteham/hospital-management/tree/1e7420e431771e3f5eec470d8a005e8255fa5fe8). This is the unchanged baseline.
- **After (overlay):** the installable additions under [A5/laravel_integration/](../../laravel_integration/), applied with `python3 A5/laravel_integration/install.py /path/to/upstream` in a separate upstream checkout. The A5 repository's pinned Git history records the after source; the overlay is not an upstream commit.
- **Tests:** `php artisan test --filter=CaseStudyIntegrationsTest` on the overlaid upstream; see [GitHub Actions](../../../.github/workflows/a5-validate.yml). This validates HTTP fakes, not external services.

## Actual files introduced by the installer

| Changed location in the upstream checkout | Change |
| --- | --- |
| `app/Services/CaseStudy/Integrations.php` | Adds `LabGateway`, `BillingGateway`, `PatientGateway` contracts and HTTP implementations |
| `app/Http/Controllers/CaseStudy/IntegrationController.php` | Adds three endpoints with validation |
| `app/Providers/CaseStudyIntegrationProvider.php` | Registers the three gateway bindings |
| `config/case_study.php` | Reads sandbox endpoints and credentials from environment |
| `routes/case_study.php` | Defines privileged lab/billing/patient endpoints |
| `tests/Feature/CaseStudyIntegrationsTest.php` | Tests payload translation, idempotency, FHIR mapping and invalid inputs |
| `bootstrap/providers.php` | Registers the new provider |
| `routes/web.php` | Includes the new route file |

The last two are the **only existing upstream files modified by the installer**. All three original booking/patient controllers remain unchanged. The installer is idempotent for its two textual registrations; run it on a clean checkout and inspect `git diff` before deployment.

## Acceptance evidence by change

| Change | Observable simulated behavior | Tests and implementation |
| --- | --- | --- |
| CH01 laboratory | Submitted booking is translated to an external order; missing required input is rejected | `test_lab_adapter_translates_payload`, `test_lab_rejects_missing_fields` |
| CH02 billing | Positive minor-unit amount is submitted with an idempotency header; zero amount is rejected | `test_billing_strategy_sends_idempotency_key`, `test_billing_rejects_zero_amount` |
| CH03 patient data | FHIR Patient name is translated to local fields; invalid resource type is rejected | `test_patient_adapter_maps_fhir`, `test_patient_rejects_invalid_fhir` |

## Refactoring and metrics interpretation

The **baseline coupling** is visible in the original controller code: booking creation and local payment-status handling are controller-level responsibilities, and there is no verified external provider abstraction. The overlay demonstrates constructor-injected gateway contracts, adapter payload translation and a configurable billing strategy. The new controller delegates to the interfaces rather than hard-coding provider HTTP schemas. The standalone Part 2 examples are independent design exercises.

**What cannot be claimed:** these are **new routes**, not behavior-preserving refactorings of existing controllers. The upstream application's original workflows were not migrated, no actual patient/booking database migration was performed, and no real vendor was called. Therefore, a full before/after comparison of *the same business workflow* (including its LOC and integration test outcomes) is **not established**. Claiming that metric or an end-to-end clinical deployment would be misleading. This is a verified **additive evolution prototype** with a remaining production-integration boundary.

See `../patterns_evolution.csv` and `../Pattern_count.csv` for version-specific pattern records; standalone and overlay counts are not additive to baseline counts.
