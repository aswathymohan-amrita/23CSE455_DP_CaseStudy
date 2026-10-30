import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Composite: API Router Tree (appRouter with sub-routers and procedures, after CH01). */
public final class RouterTree {
    private RouterTree() {}

    /** Component. */
    public sealed interface Node permits Procedure, Router {
        int count();

        /** Returns the node at parts[from..], or null. */
        Node resolve(String[] parts, int from);

        void paths(String prefix, List<String> out);

        int depth();
    }

    /** Leaf. */
    public record Procedure(String type) implements Node {
        public int count() {
            return 1;
        }

        public Node resolve(String[] parts, int from) {
            return from == parts.length ? this : null;
        }

        public void paths(String prefix, List<String> out) {
            out.add(prefix);
        }

        public int depth() {
            return 0;
        }
    }

    /** Composite. */
    public static final class Router implements Node {
        private final Map<String, Node> children = new LinkedHashMap<>();

        public Router add(String name, Node child) {
            children.put(name, child);
            return this;
        }

        public int count() {
            return children.values().stream().mapToInt(Node::count).sum();
        }

        public Node resolve(String[] parts, int from) {
            if (from == parts.length) return this;
            Node child = children.get(parts[from]);
            return child == null ? null : child.resolve(parts, from + 1);
        }

        public void paths(String prefix, List<String> out) {
            children.forEach((name, child) -> child.paths(prefix.isEmpty() ? name : prefix + "." + name, out));
        }

        public int depth() {
            return 1 + children.values().stream().mapToInt(Node::depth).max().orElse(-1);
        }
    }

    private static Router router(String... namesAndTypes) {
        Router r = new Router();
        for (int i = 0; i < namesAndTypes.length; i += 2) r.add(namesAndTypes[i], new Procedure(namesAndTypes[i + 1]));
        return r;
    }

    public static Router appRouter() {
        String q = "query", m = "mutation";
        return new Router()
                .add("user", router("getSession", q, "getCurrent", q, "getCurrentWithProfile", q, "update", m))
                .add("profile", router("getAll", q, "getOthers", q, "getOne", q, "create", m, "update", m,
                        "updatePin", m, "delete", m))
                .add("icon", router("getAll", q, "getAllUsed", q, "getAllUnused", q, "getCurrent", q))
                .add("myList", router("getAll", q, "create", m, "update", m, "delete", m))
                .add("catalogue", router("checkAccess", q));
    }

    public static List<String> pathsOf(Node node, String prefix) {
        List<String> out = new ArrayList<>();
        node.paths(prefix, out);
        return out;
    }
}
