// Part 3 - Adapter demonstration (JavaScript).
// EpicFHIRApi is simulated. This file does not call a network.

class EpicFHIRApi {
  fetchFHIRPatient(id) {
    return {
      resourceType: "Patient",
      id,
      name: [{ family: "Smith", given: ["John"] }],
      telecom: [{ system: "phone", value: "555-1234" }],
    };
  }
}

class EpicEHRAdapter {
  constructor(api) {
    this.api = api;
  }

  getPatientRecord(patientId) {
    const raw = this.api.fetchFHIRPatient(patientId);
    return {
      first_name: raw.name[0].given[0],
      last_name: raw.name[0].family,
      phone: raw.telecom[0].value,
    };
  }
}

class PatientDataService {
  constructor(provider) {
    this.provider = provider;
  }

  fetchPatient(patientId) {
    return this.provider.getPatientRecord(patientId);
  }
}

const service = new PatientDataService(new EpicEHRAdapter(new EpicFHIRApi()));
const record = service.fetchPatient("PT-98765");
console.log(record);

if (record.first_name !== "John" || record.last_name !== "Smith" || record.phone !== "555-1234") {
  process.exit(1);
}
