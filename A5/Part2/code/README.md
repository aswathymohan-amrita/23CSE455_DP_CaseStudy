# PHP roles

`LaboratoryIntegrationService` forwards a booking through `LaboratoryIntegrationInterface`. `BillingService` calls a `PaymentStrategy`. `PatientDataService` calls an `EHRProvider`.

The Java, Python, JavaScript, and C++ versions of the adapter and the strategy are in `Part3/`.
