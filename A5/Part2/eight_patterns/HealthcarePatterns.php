<?php
declare(strict_types=1);

/**
 * A5 independent, dependency-free pattern laboratory.
 * PHP 8.2+. All external systems are fakes; no patient information is persisted.
 * These are proposed additions, NOT patterns discovered in the original source.
 */
namespace A5\Patterns;

use InvalidArgumentException;
use RuntimeException;

// 01 FACADE: simplify appointment orchestration behind a single interface.
interface AppointmentStore { public function save(string $patient, string $doctor): string; }
interface NoticeSender { public function send(string $recipient, string $message): void; }
final class InMemoryAppointments implements AppointmentStore {
    public array $appointments = [];
    public function save(string $patient, string $doctor): string {
        if ($patient === '' || $doctor === '') throw new InvalidArgumentException('Missing patient or doctor');
        $id = 'APT-' . (count($this->appointments) + 1);
        $this->appointments[$id] = ['patient' => $patient, 'doctor' => $doctor];
        return $id;
    }
}
final class RecordingNoticeSender implements NoticeSender {
    public array $messages = [];
    public function send(string $recipient, string $message): void {
        $this->messages[] = ['to' => $recipient, 'message' => $message];
    }
}
final class AppointmentFacade {
    public function __construct(private AppointmentStore $store, private NoticeSender $notices) {}
    public function book(string $patient, string $doctor): string {
        $id = $this->store->save($patient, $doctor);
        $this->notices->send($patient, "Appointment $id confirmed");
        return $id;
    }
}

// 02 REPOSITORY: separate patient domain operations from storage.
final class Patient {
    public function __construct(public readonly string $id, public readonly string $name) {
        if ($id === '' || $name === '') throw new InvalidArgumentException('Invalid patient');
    }
}
interface PatientRepository {
    public function save(Patient $patient): void;
    public function find(string $id): ?Patient;
}
final class InMemoryPatientRepository implements PatientRepository {
    private array $records = [];
    public function save(Patient $patient): void { $this->records[$patient->id] = $patient; }
    public function find(string $id): ?Patient { return $this->records[$id] ?? null; }
}
final class PatientRegistry {
    public function __construct(private PatientRepository $patients) {}
    public function register(Patient $patient): void { $this->patients->save($patient); }
    public function lookup(string $id): ?Patient { return $this->patients->find($id); }
}

// 03 ADAPTER: translate vendor lab orders to a stable internal contract.
interface LaboratoryGateway { public function order(string $patientId, string $testCode): string; }
interface ExternalLabClient { public function submit(array $vendorPayload): array; }
final class FakeExternalLabClient implements ExternalLabClient {
    public array $lastPayload = [];
    public function submit(array $vendorPayload): array {
        $this->lastPayload = $vendorPayload;
        return ['externalOrderId' => 'LAB-100', 'accepted' => true];
    }
}
final class LaboratoryAdapter implements LaboratoryGateway {
    public function __construct(private ExternalLabClient $client) {}
    public function order(string $patientId, string $testCode): string {
        if ($patientId === '' || $testCode === '') throw new InvalidArgumentException('Missing lab fields');
        $response = $this->client->submit(['patient' => ['identifier' => $patientId], 'assay' => ['code' => $testCode]]);
        if (($response['accepted'] ?? false) !== true || !isset($response['externalOrderId'])) {
            throw new RuntimeException('Lab rejected order');
        }
        return $response['externalOrderId'];
    }
}

// 04 STRATEGY: interchangeable payment policies; deterministic, no real charges.
interface PaymentStrategy { public function pay(int $minorUnits, string $reference): array; }
final class FakeCardPayment implements PaymentStrategy {
    public function pay(int $minorUnits, string $reference): array {
        if ($minorUnits <= 0 || $reference === '') throw new InvalidArgumentException('Invalid payment');
        return ['provider' => 'card', 'amount_minor' => $minorUnits, 'reference' => $reference, 'status' => 'simulated'];
    }
}
final class FakeWalletPayment implements PaymentStrategy {
    public function pay(int $minorUnits, string $reference): array {
        if ($minorUnits <= 0 || $reference === '') throw new InvalidArgumentException('Invalid payment');
        return ['provider' => 'wallet', 'amount_minor' => $minorUnits, 'reference' => $reference, 'status' => 'simulated'];
    }
}
final class BillingContext {
    public function __construct(private PaymentStrategy $strategy) {}
    public function checkout(int $minorUnits, string $reference): array {
        return $this->strategy->pay($minorUnits, $reference);
    }
}

// 05 PROXY: cache patient data and avoid duplicate vendor reads.
interface PatientDataSource { public function fetch(string $patientId): array; }
final class FakePatientDataSource implements PatientDataSource {
    public int $calls = 0;
    public function fetch(string $patientId): array {
        $this->calls++;
        return ['id' => $patientId, 'name' => 'Example Patient'];
    }
}
final class CachedPatientProxy implements PatientDataSource {
    private array $cache = [];
    public function __construct(private PatientDataSource $source) {}
    public function fetch(string $patientId): array {
        if ($patientId === '') throw new InvalidArgumentException('Patient ID required');
        return $this->cache[$patientId] ??= $this->source->fetch($patientId);
    }
    public function invalidate(string $patientId): void { unset($this->cache[$patientId]); }
}

// 06 OBSERVER: notify subscribers when clinical events occur.
interface ClinicalObserver { public function onEvent(string $event, array $payload): void; }
final class ClinicalEventPublisher {
    /** @var ClinicalObserver[] */
    private array $observers = [];
    public function subscribe(ClinicalObserver $observer): void { $this->observers[spl_object_id($observer)] = $observer; }
    public function unsubscribe(ClinicalObserver $observer): void { unset($this->observers[spl_object_id($observer)]); }
    public function publish(string $event, array $payload): void {
        foreach ($this->observers as $observer) $observer->onEvent($event, $payload);
    }
}
final class ClinicalAuditObserver implements ClinicalObserver {
    public array $events = [];
    public function onEvent(string $event, array $payload): void {
        $this->events[] = ['event' => $event, 'payload' => $payload];
    }
}

// 07 FACTORY METHOD: choose an integration factory without coupling callers to clients.
interface RecordExporter { public function export(array $record): string; }
final class JsonRecordExporter implements RecordExporter {
    public function export(array $record): string {
        return json_encode($record, JSON_THROW_ON_ERROR);
    }
}
final class CsvRecordExporter implements RecordExporter {
    public function export(array $record): string {
        $fields = array_map(static fn($v): string => (string) $v, array_values($record));
        $fp = fopen('php://temp', 'r+');
        if ($fp === false) throw new RuntimeException('Cannot open temporary stream');
        fputcsv($fp, $fields);
        rewind($fp);
        $value = stream_get_contents($fp);
        fclose($fp);
        return $value;
    }
}
abstract class ExporterFactory {
    abstract protected function createExporter(): RecordExporter;
    public function exportRecord(array $record): string { return $this->createExporter()->export($record); }
}
final class JsonExporterFactory extends ExporterFactory {
    protected function createExporter(): RecordExporter { return new JsonRecordExporter(); }
}
final class CsvExporterFactory extends ExporterFactory {
    protected function createExporter(): RecordExporter { return new CsvRecordExporter(); }
}

// 08 DECORATOR: wrap a medical-record reader with audit behavior.
interface MedicalRecordReader { public function read(string $patientId): array; }
final class FakeMedicalRecordReader implements MedicalRecordReader {
    public function read(string $patientId): array { return ['patient_id' => $patientId, 'summary' => 'Synthetic record']; }
}
final class AuditedMedicalRecordReader implements MedicalRecordReader {
    public array $audit = [];
    public function __construct(private MedicalRecordReader $inner) {}
    public function read(string $patientId): array {
        if ($patientId === '') throw new InvalidArgumentException('Patient ID required');
        $record = $this->inner->read($patientId);
        $this->audit[] = ['operation' => 'read', 'patient_id' => $patientId];
        return $record;
    }
}
