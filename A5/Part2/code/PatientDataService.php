<?php

// Proposed Part 2 code. The runnable versions are in Part3/adapter.

interface EHRProvider
{
    public function getPatientRecord(string $patientId): array;
}

class PatientDataService
{
    public function __construct(private EHRProvider $provider)
    {
    }

    public function fetchPatient(string $patientId): array
    {
        return $this->provider->getPatientRecord($patientId);
    }
}
