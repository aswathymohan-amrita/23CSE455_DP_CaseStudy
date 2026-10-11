class Reader {
  read(patientId) {
    return { patient_id: patientId, summary: "synthetic" };
  }
}

class AuditedReader {
  constructor(inner) {
    this.inner = inner;
    this.audit = [];
  }

  read(patientId) {
    const record = this.inner.read(patientId);
    this.audit.push(["read", patientId]);
    return record;
  }
}

const reader = new AuditedReader(new Reader());
if (reader.read("P1").patient_id !== "P1" || reader.audit.length !== 1) {
  throw Error("decorator");
}
console.log("PASS");
