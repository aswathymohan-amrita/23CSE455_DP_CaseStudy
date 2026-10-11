import unittest

from composite import Container, Leaf


class CompositePatternTests(unittest.TestCase):
    def test_hierarchy_can_be_constructed(self) -> None:
        warehouse = hierarchy()
        self.assertEqual(warehouse.get_name(), "Warehouse")
        self.assertEqual(len(warehouse.get_children()), 2)
        self.assertEqual(len(warehouse.get_children()[0].get_children()), 2)

    def test_children_can_be_added_and_removed(self) -> None:
        container = Container("Temporary")
        location = Leaf("T-01")
        container.add_child(location)
        self.assertEqual(container.get_children(), (location,))
        self.assertTrue(container.remove_child(location))
        self.assertEqual(container.get_children(), ())

    def test_leaf_rejects_children(self) -> None:
        leaf = Leaf("A-01")
        self.assertEqual(leaf.get_children(), ())
        self.assertFalse(leaf.remove_child(Leaf("A-02")))
        with self.assertRaises(TypeError):
            leaf.add_child(Leaf("A-02"))

    def test_recursive_traversal_order(self) -> None:
        self.assertEqual(
            hierarchy().traverse(),
            ["Warehouse", "Zone-A", "A-01", "A-02", "Zone-B", "B-01"],
        )


def hierarchy() -> Container:
    warehouse = Container("Warehouse")
    zone_a = Container("Zone-A")
    zone_a.add_child(Leaf("A-01"))
    zone_a.add_child(Leaf("A-02"))
    zone_b = Container("Zone-B")
    zone_b.add_child(Leaf("B-01"))
    warehouse.add_child(zone_a)
    warehouse.add_child(zone_b)
    return warehouse


if __name__ == "__main__":
    unittest.main()
