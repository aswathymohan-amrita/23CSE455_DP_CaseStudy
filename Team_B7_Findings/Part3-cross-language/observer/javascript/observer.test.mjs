import assert from "node:assert/strict";
import { Event, Publisher, RecordingObserver } from "./observer.mjs";

const tests = [
    ["all observers receive the first event", () => {
        const { publisher, observers } = setup();
        publisher.publish(new Event("STOCK_LOW"));
        assert.deepEqual(observers.map((observer) => observer.receivedEvents.length), [1, 1, 1]);
    }],
    ["unsubscribe excludes observer 2 from the second event", () => {
        const { publisher, observers } = setup();
        publisher.publish(new Event("STOCK_LOW"));
        publisher.unsubscribe(observers[1]);
        publisher.publish(new Event("STOCK_REPLENISHED"));
        assert.deepEqual(observers.map((observer) => observer.receivedEvents.length), [2, 1, 2]);
    }],
    ["event values and object are preserved", () => {
        const { publisher, observers } = setup();
        const low = new Event("STOCK_LOW");
        const replenished = new Event("STOCK_REPLENISHED");
        publisher.publish(low);
        publisher.unsubscribe(observers[1]);
        publisher.publish(replenished);
        assert.deepEqual(
            observers.map((observer) => observer.receivedEvents.map((event) => event.type)),
            [["STOCK_LOW", "STOCK_REPLENISHED"], ["STOCK_LOW"], ["STOCK_LOW", "STOCK_REPLENISHED"]],
        );
        assert.equal(observers[0].receivedEvents[0], low);
    }],
];

function setup() {
    const publisher = new Publisher();
    const observers = [new RecordingObserver(), new RecordingObserver(), new RecordingObserver()];
    observers.forEach((observer) => publisher.subscribe(observer));
    return { publisher, observers };
}

for (const [name, test] of tests) {
    test();
    console.log(`PASS ${name}`);
}
console.log(`Observer JavaScript: ${tests.length} tests passed`);
