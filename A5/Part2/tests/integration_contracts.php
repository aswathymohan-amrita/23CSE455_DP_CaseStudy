<?php
foreach(['LaboratoryIntegrationService','QuestDiagnosticsAdapter','BillingService','PaymentProviders','PatientDataService','EpicEHRAdapter'] as $file) require_once __DIR__.'/../code/'.$file.'.php';
$n=0;
function ok(bool $v,string $label):void {global $n;if(!$v){fwrite(STDERR,"FAIL $label\n");exit(1);} $n++;echo "PASS $label\n";}
$l=new LaboratoryIntegrationService(new QuestDiagnosticsAdapter(new FakeQuestClient()));
ok($l->book(['booking_id'=>'42','patient_id'=>'P1','test_code'=>'CBC'])['external_reference']==='Q-42','lab adapter');
try{$l->book([]);ok(false,'lab validation');}catch(InvalidArgumentException $e){ok(true,'lab validation');}
$s=new BillingService(new StripePayment());$p=new BillingService(new PayPalPayment());
ok($s->charge(1200,'DX1')['provider']==='stripe','stripe');
ok($p->charge(850.5,'DX2')['provider']==='paypal','paypal');
try{$s->charge(0,'DX3');ok(false,'payment validation');}catch(InvalidArgumentException $e){ok(true,'payment validation');}
$r=(new PatientDataService(new EpicEHRAdapter(new FakeEpicFHIRApi())))->fetchPatient('PT-98765');
ok($r['first_name']==='John'&&$r['last_name']==='Smith'&&$r['phone']==='555-1234','EHR adapter');
echo "$n/$n passed\n";
