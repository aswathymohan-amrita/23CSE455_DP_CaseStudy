/**
 * Part 3 - Adapter demonstration (Java).
 * Proposed design. EpicFHIRApi is a simulated adaptee, not a live integration.
 */

import java.util.List;
import java.util.Map;

interface EHRProvider {
    Map<String, String> getPatientRecord(String patientId);
}

class EpicFHIRApi {
    Map<String, Object> fetchFHIRPatient(String id) {
        return Map.of(
                "resourceType", "Patient",
                "id", id,
                "name", List.of(Map.of("family", "Smith", "given", List.of("John"))),
                "telecom", List.of(Map.of("system", "phone", "value", "555-1234")));
    }
}

class EpicEHRAdapter implements EHRProvider {
    private final EpicFHIRApi api;

    EpicEHRAdapter(EpicFHIRApi api) {
        this.api = api;
    }

    @Override
    @SuppressWarnings("unchecked")
    public Map<String, String> getPatientRecord(String patientId) {
        Map<String, Object> raw = api.fetchFHIRPatient(patientId);
        List<Map<String, Object>> names = (List<Map<String, Object>>) raw.get("name");
        List<String> given = (List<String>) names.get(0).get("given");
        List<Map<String, String>> telecom = (List<Map<String, String>>) raw.get("telecom");

        return Map.of(
                "first_name", given.get(0),
                "last_name", String.valueOf(names.get(0).get("family")),
                "phone", telecom.get(0).get("value"));
    }
}

class PatientDataService {
    private final EHRProvider provider;

    PatientDataService(EHRProvider provider) {
        this.provider = provider;
    }

    Map<String, String> fetchPatient(String patientId) {
        return provider.getPatientRecord(patientId);
    }
}

public class AdapterDemo {
    public static void main(String[] args) {
        PatientDataService service = new PatientDataService(new EpicEHRAdapter(new EpicFHIRApi()));
        System.out.println(service.fetchPatient("PT-98765"));
    }
}
