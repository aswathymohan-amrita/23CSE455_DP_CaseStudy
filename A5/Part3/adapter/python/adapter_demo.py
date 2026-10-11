"""Part 3 - Adapter demonstration (Python).

Proposed design for the hospital-management case study.
EpicFHIRApi simulates an external EHR. It does not call a network.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EHRProvider(ABC):
    @abstractmethod
    def get_patient_record(self, patient_id: str) -> dict[str, str]:
        raise NotImplementedError


class EpicFHIRApi:
    def fetch_fhir_patient(self, patient_id: str) -> dict:
        return {
            "resourceType": "Patient",
            "id": patient_id,
            "name": [{"family": "Smith", "given": ["John"]}],
            "telecom": [{"system": "phone", "value": "555-1234"}],
        }


class EpicEHRAdapter(EHRProvider):
    def __init__(self, api: EpicFHIRApi) -> None:
        self._api = api

    def get_patient_record(self, patient_id: str) -> dict[str, str]:
        raw = self._api.fetch_fhir_patient(patient_id)
        return {
            "first_name": raw["name"][0]["given"][0],
            "last_name": raw["name"][0]["family"],
            "phone": raw["telecom"][0]["value"],
        }


class PatientDataService:
    def __init__(self, provider: EHRProvider) -> None:
        self._provider = provider

    def fetch_patient(self, patient_id: str) -> dict[str, str]:
        return self._provider.get_patient_record(patient_id)


if __name__ == "__main__":
    service = PatientDataService(EpicEHRAdapter(EpicFHIRApi()))
    print(service.fetch_patient("PT-98765"))
