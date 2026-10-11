class JsonExporter {
  export(record) {
    return JSON.stringify(record);
  }
}

class CsvExporter {
  export(record) {
    return Object.values(record).join(",") + "\n";
  }
}

class Factory {
  constructor(kind) {
    this.kind = kind;
  }

  createExporter() {
    return this.kind === "json" ? new JsonExporter() : new CsvExporter();
  }

  export(record) {
    return this.createExporter().export(record);
  }
}

if (
  !new Factory("json").export({ id: "P1" }).includes("P1") ||
  !new Factory("csv").export({ id: "P1" }).includes("P1")
) {
  throw Error("factory");
}
console.log("PASS");
