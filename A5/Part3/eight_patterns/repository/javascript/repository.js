class Repo {
  constructor() {
    this.rows = new Map();
  }

  save(patient) {
    this.rows.set(patient.id, patient);
  }

  find(id) {
    return this.rows.get(id) || null;
  }
}

class Registry {
  constructor(repository) {
    this.repository = repository;
  }

  register(patient) {
    this.repository.save(patient);
  }

  lookup(id) {
    return this.repository.find(id);
  }
}

const registry = new Registry(new Repo());
registry.register({ id: "P1", name: "Demo" });
if (registry.lookup("P1").name !== "Demo" || registry.lookup("none") !== null) {
  throw Error("repository");
}
console.log("PASS");
