import java.util.List;

public class CompositePatternTest {

    public static void main(String[] args) {
        testHierarchyCanBeConstructed();
        testChildrenCanBeAddedAndRemoved();
        testLeafRejectsChildren();
        testRecursiveTraversalOrder();
        System.out.println("Composite Java: 4 tests passed");
    }

    private static void testHierarchyCanBeConstructed() {
        var warehouse = hierarchy();
        check(warehouse.getName().equals("Warehouse"), "root name");
        check(warehouse.getChildren().size() == 2, "root has two zones");
        check(warehouse.getChildren().get(0).getChildren().size() == 2, "Zone-A has two locations");
    }

    private static void testChildrenCanBeAddedAndRemoved() {
        var container = new CompositePattern.Container("Temporary");
        var leaf = new CompositePattern.Leaf("T-01");
        container.addChild(leaf);
        check(container.getChildren().equals(List.of(leaf)), "child added");
        check(container.removeChild(leaf), "child removed");
        check(container.getChildren().isEmpty(), "child list empty after removal");
    }

    private static void testRecursiveTraversalOrder() {
        check(hierarchy().traverse().equals(List.of(
                "Warehouse", "Zone-A", "A-01", "A-02", "Zone-B", "B-01")), "preorder traversal");
    }

    private static void testLeafRejectsChildren() {
        var leaf = new CompositePattern.Leaf("A-01");
        check(leaf.getChildren().isEmpty(), "leaf has no children");
        check(!leaf.removeChild(new CompositePattern.Leaf("A-02")), "leaf cannot remove children");
        try {
            leaf.addChild(new CompositePattern.Leaf("A-02"));
            throw new AssertionError("leaf must reject addChild");
        } catch (UnsupportedOperationException expected) {
            check(true, "leaf rejects addChild");
        }
    }

    private static CompositePattern.Container hierarchy() {
        var warehouse = new CompositePattern.Container("Warehouse");
        var zoneA = new CompositePattern.Container("Zone-A");
        zoneA.addChild(new CompositePattern.Leaf("A-01"));
        zoneA.addChild(new CompositePattern.Leaf("A-02"));
        var zoneB = new CompositePattern.Container("Zone-B");
        zoneB.addChild(new CompositePattern.Leaf("B-01"));
        warehouse.addChild(zoneA);
        warehouse.addChild(zoneB);
        return warehouse;
    }

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}
