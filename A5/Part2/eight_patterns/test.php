<?php
declare(strict_types=1);
require_once __DIR__ . '/HealthcarePatterns.php';
use A5\Patterns\{InMemoryAppointments,RecordingNoticeSender,AppointmentFacade,Patient,InMemoryPatientRepository,PatientRegistry,FakeExternalLabClient,LaboratoryAdapter,BillingContext,FakeCardPayment,FakeWalletPayment,FakePatientDataSource,CachedPatientProxy,ClinicalEventPublisher,ClinicalAuditObserver,JsonExporterFactory,CsvExporterFactory,FakeMedicalRecordReader,AuditedMedicalRecordReader};
$count = 0;
function verify(bool $ok, string $label): void { global $count; if (!$ok) { fwrite(STDERR, "FAIL: $label\n"); exit(1); } $count++; echo "PASS: $label\n"; }
$store = new InMemoryAppointments(); $sender = new RecordingNoticeSender();
$id = (new AppointmentFacade($store, $sender))->book('PT1', 'DR1');
verify($id === 'APT-1' && count($sender->messages) === 1, 'Facade coordinates appointment and notice');
$repo = new InMemoryPatientRepository(); $registry = new PatientRegistry($repo);
$registry->register(new Patient('PT1','Demo Patient'));
verify($registry->lookup('PT1')?->name === 'Demo Patient' && $registry->lookup('missing') === null, 'Repository persistence contract');
$vendor = new FakeExternalLabClient();
verify((new LaboratoryAdapter($vendor))->order('PT1','CBC') === 'LAB-100' && $vendor->lastPayload['assay']['code'] === 'CBC', 'Adapter maps lab payload');
verify((new BillingContext(new FakeCardPayment()))->checkout(1500,'B1')['provider'] === 'card', 'Strategy card');
verify((new BillingContext(new FakeWalletPayment()))->checkout(1500,'B1')['provider'] === 'wallet', 'Strategy wallet');
$source = new FakePatientDataSource(); $proxy = new CachedPatientProxy($source);
$proxy->fetch('PT1'); $proxy->fetch('PT1');
verify($source->calls === 1, 'Proxy caches reads');
$proxy->invalidate('PT1'); $proxy->fetch('PT1');
verify($source->calls === 2, 'Proxy invalidates stale record');
$publisher = new ClinicalEventPublisher(); $observer = new ClinicalAuditObserver(); $publisher->subscribe($observer);
$publisher->publish('prescription.created', ['patient_id'=>'PT1']);
verify(count($observer->events) === 1, 'Observer receives event');
$publisher->unsubscribe($observer); $publisher->publish('other', []);
verify(count($observer->events) === 1, 'Observer unsubscribe');
verify((new JsonExporterFactory())->exportRecord(['id'=>'PT1']) === '{"id":"PT1"}', 'Factory Method JSON');
verify(str_contains((new CsvExporterFactory())->exportRecord(['id'=>'PT1']), 'PT1'), 'Factory Method CSV');
$audited = new AuditedMedicalRecordReader(new FakeMedicalRecordReader());
verify($audited->read('PT1')['patient_id'] === 'PT1' && count($audited->audit) === 1, 'Decorator records read audit');
try { (new BillingContext(new FakeCardPayment()))->checkout(0,'B1'); verify(false,'Invalid payment rejected'); }
catch (InvalidArgumentException $e) { verify(true,'Invalid payment rejected'); }
try { (new LaboratoryAdapter($vendor))->order('','CBC'); verify(false,'Invalid lab order rejected'); }
catch (InvalidArgumentException $e) { verify(true,'Invalid lab order rejected'); }
echo "$count assertions passed\n";
