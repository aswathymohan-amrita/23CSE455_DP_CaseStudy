class Store {
  constructor() {
    this.rows = [];
  }

  save(patient, doctor) {
    this.rows.push([patient, doctor]);
    return this.rows.length;
  }
}

class Notice {
  constructor() {
    this.sent = [];
  }

  send(patient, message) {
    this.sent.push([patient, message]);
  }
}

class Facade {
  constructor(store, notice) {
    this.store = store;
    this.notice = notice;
  }

  book(patient, doctor) {
    if (!patient || !doctor) {
      throw Error("missing");
    }
    const id = this.store.save(patient, doctor);
    this.notice.send(patient, String(id));
    return id;
  }
}

const store = new Store();
const notice = new Notice();
if (new Facade(store, notice).book("P1", "D1") !== 1 || notice.sent.length !== 1) {
  throw Error("facade");
}
console.log("PASS");
