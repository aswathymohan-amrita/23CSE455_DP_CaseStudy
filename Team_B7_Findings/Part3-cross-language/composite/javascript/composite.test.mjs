import assert from "node:assert/strict";
import { Container, Leaf } from "./composite.mjs";

const expected = ["Warehouse", "Zone-A", "A-01", "A-02", "Zone-B", "B-01"];
const tests = [
    ["hierarchy can be constructed", () => {
        const warehouse = hierarchy();
        assert.equal(warehouse.getName(), "Warehouse");
        assert.equal(warehouse.getChildren().length, 2);
        assert.equal(warehouse.getChildren()[0].getChildren().length, 2);
    }],
    ["children can be added and removed", () => {
        const container = new Container("Temporary");
        const location = new Leaf("T-01");
        container.addChild(location);
        assert.deepEqual(container.getChildren(), [location]);
        assert.equal(container.removeChild(location), true);
        assert.deepEqual(container.getChildren(), []);
    }],
    ["leaf rejects children", () => {
        const leaf = new Leaf("A-01");
        assert.deepEqual(leaf.getChildren(), []);
        assert.equal(leaf.removeChild(new Leaf("A-02")), false);
        assert.throws(() => leaf.addChild(new Leaf("A-02")), TypeError);
    }],
    ["recursive traversal is preorder", () => {
        assert.deepEqual(hierarchy().traverse(), expected);
    }],
];

function hierarchy() {
    const warehouse = new Container("Warehouse");
    const zoneA = new Container("Zone-A");
    zoneA.addChild(new Leaf("A-01"));
    zoneA.addChild(new Leaf("A-02"));
    const zoneB = new Container("Zone-B");
    zoneB.addChild(new Leaf("B-01"));
    warehouse.addChild(zoneA);
    warehouse.addChild(zoneB);
    return warehouse;
}

for (const [name, test] of tests) {
    test();
    console.log(`PASS ${name}`);
}
console.log(`Composite JavaScript: ${tests.length} tests passed`);
