class Observer {
  constructor() {
    this.events = [];
  }

  update(event) {
    this.events.push(event);
  }
}

class Publisher {
  constructor() {
    this.subscribers = new Set();
  }

  subscribe(observer) {
    this.subscribers.add(observer);
  }

  unsubscribe(observer) {
    this.subscribers.delete(observer);
  }

  publish(event) {
    for (const observer of this.subscribers) {
      observer.update(event);
    }
  }
}

const publisher = new Publisher();
const observer = new Observer();
publisher.subscribe(observer);
publisher.publish("lab.ready");
publisher.unsubscribe(observer);
publisher.publish("other");

if (observer.events.join() !== "lab.ready") {
  throw Error("observer");
}
console.log("PASS");
