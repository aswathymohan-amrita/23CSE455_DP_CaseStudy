import java.util.ArrayList;
import java.util.List;

final class CompositePattern {

    interface Component {
        String getName();

        void addChild(Component child);

        boolean removeChild(Component child);

        List<Component> getChildren();

        List<String> traverse();
    }

    static final class Leaf implements Component {
        private final String name;

        Leaf(String name) {
            this.name = name;
        }

        @Override
        public String getName() {
            return name;
        }

        @Override
        public void addChild(Component child) {
            throw new UnsupportedOperationException("A location leaf cannot contain children");
        }

        @Override
        public boolean removeChild(Component child) {
            return false;
        }

        @Override
        public List<Component> getChildren() {
            return List.of();
        }

        @Override
        public List<String> traverse() {
            return List.of(name);
        }
    }

    static final class Container implements Component {
        private final String name;
        private final List<Component> children = new ArrayList<>();

        Container(String name) {
            this.name = name;
        }

        @Override
        public String getName() {
            return name;
        }

        @Override
        public void addChild(Component child) {
            children.add(child);
        }

        @Override
        public boolean removeChild(Component child) {
            return children.remove(child);
        }

        @Override
        public List<Component> getChildren() {
            return List.copyOf(children);
        }

        @Override
        public List<String> traverse() {
            var names = new ArrayList<String>();
            names.add(name);
            for (Component child : children) {
                names.addAll(child.traverse());
            }
            return names;
        }
    }
}
