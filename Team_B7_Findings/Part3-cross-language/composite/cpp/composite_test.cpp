#include "composite.hpp"

#include <cassert>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

std::shared_ptr<Container> hierarchy() {
    auto warehouse = std::make_shared<Container>("Warehouse");
    auto zone_a = std::make_shared<Container>("Zone-A");
    zone_a->addChild(std::make_shared<Leaf>("A-01"));
    zone_a->addChild(std::make_shared<Leaf>("A-02"));
    auto zone_b = std::make_shared<Container>("Zone-B");
    zone_b->addChild(std::make_shared<Leaf>("B-01"));
    warehouse->addChild(zone_a);
    warehouse->addChild(zone_b);
    return warehouse;
}

void test_hierarchy_can_be_constructed() {
    auto warehouse = hierarchy();
    assert(warehouse->getName() == "Warehouse");
    assert(warehouse->getChildren().size() == 2);
    assert(warehouse->getChildren()[0]->getChildren().size() == 2);
}

void test_children_can_be_added_and_removed() {
    auto container = std::make_shared<Container>("Temporary");
    auto location = std::make_shared<Leaf>("T-01");
    container->addChild(location);
    assert(container->getChildren().size() == 1);
    assert(container->removeChild(location));
    assert(container->getChildren().empty());
}

void test_leaf_rejects_children() {
    auto leaf = std::make_shared<Leaf>("A-01");
    assert(leaf->getChildren().empty());
    assert(!leaf->removeChild(std::make_shared<Leaf>("A-02")));
    bool rejected = false;
    try {
        leaf->addChild(std::make_shared<Leaf>("A-02"));
    } catch (const std::logic_error&) {
        rejected = true;
    }
    assert(rejected);
}

void test_recursive_traversal_order() {
    const std::vector<std::string> expected{
        "Warehouse", "Zone-A", "A-01", "A-02", "Zone-B", "B-01"};
    assert(hierarchy()->traverse() == expected);
}

int main() {
    test_hierarchy_can_be_constructed();
    test_children_can_be_added_and_removed();
    test_leaf_rejects_children();
    test_recursive_traversal_order();
    std::cout << "Composite C++: 4 tests passed\n";
}
