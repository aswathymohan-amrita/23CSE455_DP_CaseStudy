import java.util.*;

public final class DiagramSystem {
    interface Block { List<String> names(); }
    static final class Node implements Block {
        private final String name;
        Node(String name) { this.name = name; }
        public List<String> names() { return List.of(name); }
    }
    static final class Group implements Block {
        final List<Block> children = new ArrayList<>();
        public List<String> names() {
            List<String> result = new ArrayList<>();
            for (Block child : children) result.addAll(child.names());
            return result;
        }
    }
    interface Model { void add(String name); }
    static class Diagram implements Model {
        final Group root = new Group();
        final Deque<Group> stack = new ArrayDeque<>();
        final List<String> links = new ArrayList<>();
        Diagram() { stack.push(root); }
        public void add(String name) {
            if (root.names().contains(name)) throw new IllegalArgumentException("duplicate");
            stack.peek().children.add(new Node(name));
        }
        void link(String left, String right) {
            List<String> names = root.names();
            if (!names.contains(left) || !names.contains(right))
                throw new IllegalArgumentException("missing endpoint");
            links.add(left + "->" + right);
        }
    }
    interface Command { void execute(Diagram model, String[] args); }
    static final class Create implements Command {
        public void execute(Diagram model, String[] args) { model.add(args[0]); }
    }
    static final class Link implements Command {
        public void execute(Diagram model, String[] args) { model.link(args[0], args[1]); }
    }
    static final class OpenGroup implements Command {
        public void execute(Diagram model, String[] args) {
            Group group = new Group();
            model.stack.peek().children.add(group);
            model.stack.push(group);
        }
    }
    static final class CloseGroup implements Command {
        public void execute(Diagram model, String[] args) {
            if (model.stack.size() == 1) throw new IllegalArgumentException("unmatched end");
            model.stack.pop();
        }
    }
    static abstract class Parser {
        final Map<String, Command> commands = Map.of("class", new Create(), "link", new Link(),
                "group", new OpenGroup(), "end", new CloseGroup());
        final Map<String, Integer> arities = Map.of("class", 1, "link", 2, "group", 0, "end", 0);
        protected abstract Diagram createModel();
        Diagram parse(List<String> lines) {
            Diagram model = createModel();
            for (String line : lines) {
                if (line.trim().isEmpty()) continue;
                String[] words = line.trim().split("\\s+");
                Command command = commands.get(words[0]);
                if (command == null) throw new IllegalArgumentException("syntax");
                if (words.length != arities.get(words[0]) + 1) throw new IllegalArgumentException("syntax");
                command.execute(model, Arrays.copyOfRange(words, 1, words.length));
            }
            if (model.stack.size() != 1) throw new IllegalArgumentException("unclosed group");
            return model;
        }
    }
    static final class DiagramParser extends Parser {
        protected Diagram createModel() { return new Diagram(); }
    }
    interface Renderer { String render(Diagram model); }
    static final class Compact implements Renderer {
        public String render(Diagram model) {
            return String.join(",", model.root.names()) + "|" + String.join(",", model.links);
        }
    }
    static final class Bracketed implements Renderer {
        public String render(Diagram model) {
            List<String> names = new ArrayList<>();
            for (String name : model.root.names()) names.add("[" + name + "]");
            return String.join(",", names) + "|" + String.join(",", model.links);
        }
    }
    static final class LegacyNames {
        String encode(List<String> names) {
            List<String> quoted = new ArrayList<>();
            for (String name : names)
                quoted.add("\"" + name.replace("\\", "\\\\").replace("\"", "\\\"") + "\"");
            return "[" + String.join(",", quoted) + "]";
        }
    }
    static final class NamesAdapter implements Renderer {
        final LegacyNames legacy = new LegacyNames();
        public String render(Diagram model) { return legacy.encode(model.root.names()); }
    }
    static final class Exporter {
        final Renderer renderer;
        Exporter(Renderer renderer) { this.renderer = renderer; }
        String export(Diagram model) { return renderer.render(model); }
    }
}
