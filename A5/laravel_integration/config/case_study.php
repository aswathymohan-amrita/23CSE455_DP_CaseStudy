<?php
return [
 'lab'=>['url'=>env('CASE_STUDY_LAB_URL','http://127.0.0.1:9999/lab'),'token'=>env('CASE_STUDY_LAB_TOKEN','')],
 'billing'=>['url'=>env('CASE_STUDY_BILLING_URL','http://127.0.0.1:9999/billing'),'token'=>env('CASE_STUDY_BILLING_TOKEN',''),'provider'=>env('CASE_STUDY_BILLING_PROVIDER','sandbox')],
 'patient'=>['url'=>env('CASE_STUDY_FHIR_URL','http://127.0.0.1:9999/fhir'),'token'=>env('CASE_STUDY_FHIR_TOKEN','')],
];
