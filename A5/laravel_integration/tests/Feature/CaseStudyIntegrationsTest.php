<?php
namespace Tests\Feature;
use Tests\TestCase;
use Illuminate\Support\Facades\Http;
use App\Services\CaseStudy\{LabGateway,BillingGateway,PatientGateway};

final class CaseStudyIntegrationsTest extends TestCase {
 public function test_lab_adapter_translates_payload(): void {
  Http::fake(['*'=>Http::response(['orderId'=>'LAB-42','status'=>'accepted'])]);
  $result=app(LabGateway::class)->submit(['booking_id'=>'B1','patient_id'=>'P1','test_code'=>'CBC']);
  $this->assertSame('LAB-42',$result['external_reference']);
  Http::assertSent(fn($req)=>$req['assay']['code']==='CBC' && $req['subject']['identifier']==='P1');
 }
 public function test_billing_strategy_sends_idempotency_key(): void {
  Http::fake(['*'=>Http::response(['transaction_id'=>'TX-1','status'=>'pending'])]);
  $result=app(BillingGateway::class)->charge(2500,'REF-1');
  $this->assertSame('TX-1',$result['transaction_id']);
  Http::assertSent(fn($req)=>$req->hasHeader('Idempotency-Key','REF-1'));
 }
 public function test_patient_adapter_maps_fhir(): void {
  Http::fake(['*'=>Http::response(['resourceType'=>'Patient','id'=>'P1',
   'name'=>[['given'=>['Demo'],'family'=>'Person']]])]);
  $result=app(PatientGateway::class)->fetch('P1');
  $this->assertSame('Demo',$result['first_name']);
  $this->assertSame('Person',$result['last_name']);
 }
 public function test_lab_rejects_missing_fields(): void {
  $this->expectException(\InvalidArgumentException::class);
  app(LabGateway::class)->submit([]);
 }
 public function test_billing_rejects_zero_amount(): void {
  $this->expectException(\InvalidArgumentException::class);
  app(BillingGateway::class)->charge(0,'REF-1');
 }
 public function test_patient_rejects_invalid_fhir(): void {
  Http::fake(['*'=>Http::response(['resourceType'=>'Observation'])]);
  $this->expectException(\RuntimeException::class);
  app(PatientGateway::class)->fetch('P1');
 }
}
