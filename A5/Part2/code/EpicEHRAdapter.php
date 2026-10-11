<?php
interface EpicFHIRApi { public function fetch(string $patientId): array; }
final class FakeEpicFHIRApi implements EpicFHIRApi {
 public function fetch(string $patientId): array { return ['id'=>$patientId,'name'=>[['given'=>['John'],'family'=>'Smith']],'telecom'=>[['value'=>'555-1234']]]; }
}
final class EpicEHRAdapter implements EHRProvider {
 public function __construct(private EpicFHIRApi $api) {}
 public function getPatientRecord(string $patientId): array {
  if($patientId==='') throw new InvalidArgumentException('Missing patient ID');
  $r=$this->api->fetch($patientId);
  return ['patient_id'=>$r['id'],'first_name'=>$r['name'][0]['given'][0]??'','last_name'=>$r['name'][0]['family']??'','phone'=>$r['telecom'][0]['value']??''];
 }
}
