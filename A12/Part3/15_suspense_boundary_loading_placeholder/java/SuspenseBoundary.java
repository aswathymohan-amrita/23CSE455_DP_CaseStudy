import java.util.ArrayList;
import java.util.List;
import java.util.TreeSet;
import java.util.function.Supplier;

/** Suspense Boundary: Shows Loading Placeholder ((shows)/loading.tsx as the Suspense fallback of async pages). */
public final class SuspenseBoundary {
    /** Thrown by a child that is still waiting for data (React's suspend signal). */
    static final class Pending extends RuntimeException {}

    static final class FetchError extends RuntimeException {
        FetchError(String name) {
            super(name);
        }
    }

    interface Node {
        String render(int t);
    }

    record Dependency(String name, int ms, boolean fails) {}

    /** Async server page: awaits all its fetches (Promise.all) before it can render. */
    record AsyncPage(List<Dependency> deps) implements Node {
        public String render(int t) {
            if (deps.stream().anyMatch(d -> d.ms() > t)) throw new Pending();
            deps.stream().filter(Dependency::fails).findFirst().ifPresent(d -> {
                throw new FetchError(d.name());
            });
            return "page(rows=" + deps.size() + ")";
        }
    }

    /** Renders the fallback while the child suspends; other errors pass through. */
    record Boundary(Node child, Supplier<String> fallback) implements Node {
        public String render(int t) {
            try {
                return child.render(t);
            } catch (Pending p) {
                return fallback.get();
            }
        }
    }

    /** Next.js LoadingBoundary: Suspense only if the segment has loading.tsx. */
    static Node segment(AsyncPage page, boolean hasLoading) {
        return hasLoading ? new Boundary(page, () -> "loading") : page;
    }

    /** Server streaming: render at every point in time where something can change; emit changed frames. */
    static List<String> stream(Node root, List<Dependency> deps) {
        TreeSet<Integer> times = new TreeSet<>();
        times.add(0);
        deps.forEach(d -> times.add(d.ms()));
        List<String> frames = new ArrayList<>();
        String last = null;
        for (int t : times) {
            String view;
            try {
                view = root.render(t);
            } catch (Pending p) { // no boundary: nothing can be sent yet
                continue;
            } catch (FetchError e) { // handled by the segment error boundary
                view = "error(" + e.getMessage() + ")";
            }
            if (!view.equals(last)) {
                frames.add("t=" + t + ":" + view);
                last = view;
            }
            if (!view.equals("loading")) break; // final frame sent
        }
        return frames;
    }
}
