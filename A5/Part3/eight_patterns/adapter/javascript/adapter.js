class Vendor {
  submit(payload) {
    return { accepted: true, id: "LAB-1", payload };
  }
}

class Adapter {
  constructor(vendor) {
    this.vendor = vendor;
  }

  order(patientId, testCode) {
    if (!patientId || !testCode) {
      throw Error("missing");
    }

    const response = this.vendor.submit({
      patient: { id: patientId },
      test: { code: testCode },
    });

    if (!response.accepted) {
      throw Error("rejected");
    }
    return response.id;
  }
}

if (new Adapter(new Vendor()).order("P1", "CBC") !== "LAB-1") {
  throw Error("adapter");
}
console.log("PASS");
