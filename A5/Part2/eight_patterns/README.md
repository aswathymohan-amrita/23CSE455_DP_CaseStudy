# Eight-pattern healthcare extension — A5

**Scope:** Standalone, executable PHP 8.2+ examples inspired by the original Laravel healthcare domain. They are *proposed* designs, not patterns discovered in the original application and not themselves integrated with Laravel routes, databases or third-party APIs. A **separate** installable Laravel overlay under `../../laravel_integration/` implements three related HTTP integration boundaries and tests them using simulated responses; it does not wire these standalone examples directly into existing booking controllers. All data and external providers are synthetic.

## Team allocation (proposed, not a claim about individual authorship)

| Member | Pattern A | Pattern B | Use case |
|---|---|---|---|
| Nemali Ashrith Reddy | Facade | Repository | Appointments and patient records |
| Akshay Reddy Velugati | Adapter | Strategy | Laboratory integration and billing |
| B. Pravallika | Proxy | Observer | Cached patient lookup and notifications |
| Daripineni Manogna | Factory Method | Decorator | Medical record export and read auditing |

**Execution:** `php Part2/eight_patterns/test.php` from the A5 folder, or `php test.php` from this directory. No dependencies or credentials required. The test suite checks 14 assertions, including negative paths. Run the command before recording pass results.

## Source mapping and pattern roles

| Pattern | Context/client | Abstraction | Concrete collaborators |
|---|---|---|---|
| Facade | AppointmentFacade::book | AppointmentStore, NoticeSender | InMemoryAppointments, RecordingNoticeSender |
| Repository | PatientRegistry | PatientRepository | InMemoryPatientRepository, Patient |
| Adapter | LaboratoryAdapter::order | LaboratoryGateway, ExternalLabClient | FakeExternalLabClient |
| Strategy | BillingContext::checkout | PaymentStrategy | FakeCardPayment, FakeWalletPayment |
| Proxy | CachedPatientProxy::fetch | PatientDataSource | FakePatientDataSource |
| Observer | ClinicalEventPublisher::publish | ClinicalObserver | ClinicalAuditObserver |
| Factory Method | ExporterFactory::exportRecord | RecordExporter | JsonExporterFactory, CsvExporterFactory |
| Decorator | AuditedMedicalRecordReader::read | MedicalRecordReader | FakeMedicalRecordReader |

**Architecture:** These standalone examples illustrate domain service/facade -> interface -> collaborator. The later `../../laravel_integration/` adds separate protected Laravel controller endpoints and DI bindings for lab, billing and patient data; integration into existing booking/record workflows remains future work.

## Real integration checklist

For Laravel integration: introduce PSR-4 namespaces and service-provider bindings; preserve existing routes and authorization; validate patient consent and access control; use encrypted storage and audit retention policies; configure provider secrets via environment variables; add HTTP timeouts/retries/idempotency and webhook signature verification; test against a staging sandbox; implement transactional boundaries and compensating actions for failed payments. A local fake's simulated success is not a real payment or external booking.

## Attribution and reproducibility

The allocation is a proposed team division, **not evidence** that each named student authored or tested the corresponding code. Source contributions must be confirmed by the team. This new set is distinct from A8's NestJS examples and from the original A5 baseline Active Record and framework Facade findings. Avoid counting the same Facade twice across baseline and extension without identifying the different collaboration.
