// Part 3 - Adapter demonstration (C++).
// EpicFHIRApi is simulated. This program does not call a network.

#include <iostream>
#include <string>
#include <vector>

struct PatientRecord {
    std::string first_name;
    std::string last_name;
    std::string phone;
};

class EHRProvider {
public:
    virtual ~EHRProvider() = default;
    virtual PatientRecord getPatientRecord(const std::string& patientId) = 0;
};

struct FhirName {
    std::string family;
    std::string given;
};

struct FhirContact {
    std::string value;
};

struct FhirPatient {
    std::string id;
    std::vector<FhirName> name;
    std::vector<FhirContact> telecom;
};

class EpicFHIRApi {
public:
    FhirPatient fetchFHIRPatient(const std::string& id) const {
        return {id, {{"Smith", "John"}}, {{"555-1234"}}};
    }
};

class EpicEHRAdapter : public EHRProvider {
public:
    explicit EpicEHRAdapter(const EpicFHIRApi& api) : api_(api) {}

    PatientRecord getPatientRecord(const std::string& patientId) override {
        const FhirPatient raw = api_.fetchFHIRPatient(patientId);
        return {raw.name.at(0).given, raw.name.at(0).family, raw.telecom.at(0).value};
    }

private:
    EpicFHIRApi api_;
};

class PatientDataService {
public:
    explicit PatientDataService(EHRProvider& provider) : provider_(provider) {}

    PatientRecord fetchPatient(const std::string& patientId) {
        return provider_.getPatientRecord(patientId);
    }

private:
    EHRProvider& provider_;
};

int main() {
    EpicFHIRApi api;
    EpicEHRAdapter adapter(api);
    PatientDataService service(adapter);
    const PatientRecord record = service.fetchPatient("PT-98765");
    std::cout << record.first_name << " " << record.last_name << " " << record.phone << "\n";
    if (record.first_name != "John" || record.last_name != "Smith" || record.phone != "555-1234") {
        return 1;
    }
    return 0;
}
