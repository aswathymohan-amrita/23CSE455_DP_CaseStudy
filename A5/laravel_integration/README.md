# Laravel integration overlay for original hospital-management

This is an **installable Laravel 12 overlay**, based on the original project at commit `1e7420e431771e3f5eec470d8a005e8255fa5fe8`. The A5 repository does not contain the full upstream application. Apply this overlay to a clean, separately checked-out upstream application using:

```sh
python3 A5/laravel_integration/install.py /path/to/hospital-management
cd /path/to/hospital-management
composer install
php artisan test --filter=CaseStudyIntegrationsTest
php artisan route:list --path=case-study
```

The installation copies three HTTP integration components, their contracts, Laravel controller, provider bindings, config, restricted routes and six Laravel feature tests. It patches `bootstrap/providers.php` and `routes/web.php` in the target checkout. It does not alter existing booking controllers, so it is **an integrated additional route surface**, not a replacement of existing booking, payment or medical-record workflows. Review the target checkout's `git diff` and run tests before deployment.

All three gateways make HTTP calls to configured endpoints. Tests use Laravel `Http::fake()`; no real lab, payment or FHIR provider was accessed. The default localhost URLs intentionally point to nonrunning endpoints. Provide only staging credentials via environment variables, never commit them. The privileged admin route middleware uses the upstream's existing `role:admin` middleware. Patient records and billing require further policy, consent, audit, idempotency and production security review.

This overlay is **not evidence of a successful full Laravel test run** until `php artisan test` has executed in a real upstream checkout. CI may validate syntax and unit contracts separately. Source mapping and integration status must be reported accordingly.
