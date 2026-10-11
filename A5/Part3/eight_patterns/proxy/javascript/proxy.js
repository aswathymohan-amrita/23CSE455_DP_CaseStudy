class Source {
  constructor() {
    this.calls = 0;
  }

  fetch(patientId) {
    this.calls++;
    return { id: patientId };
  }
}

class Proxy {
  constructor(source) {
    this.source = source;
    this.cache = new Map();
  }

  fetch(patientId) {
    if (!this.cache.has(patientId)) {
      this.cache.set(patientId, this.source.fetch(patientId));
    }
    return this.cache.get(patientId);
  }

  invalidate(patientId) {
    this.cache.delete(patientId);
  }
}

const source = new Source();
const proxy = new Proxy(source);
proxy.fetch("P1");
proxy.fetch("P1");
if (source.calls !== 1) {
  throw Error("cache");
}
proxy.invalidate("P1");
proxy.fetch("P1");
if (source.calls !== 2) {
  throw Error("invalidate");
}
console.log("PASS");
