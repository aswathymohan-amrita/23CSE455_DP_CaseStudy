import java.util.Map;
import java.util.function.Function;
import java.util.function.Supplier;

/** Error Boundary: Shows Segment Error Boundary + Root Global Error Boundary (error.tsx / global-error.tsx). */
public final class ErrorBoundaryApp {
    static final class RenderError extends RuntimeException {
        RenderError(String message) {
            super(message);
        }
    }

    interface Component {
        String render();
    }

    /** A component that throws for its first `fails` renders. */
    static final class Flaky implements Component {
        private final int fails;
        private final String message;
        private final Supplier<String> view;
        private int renders;

        Flaky(int fails, String message, Supplier<String> view) {
            this.fails = fails;
            this.message = message;
            this.view = view;
        }

        public String render() {
            renders++;
            if (renders <= fails) throw new RenderError(message);
            return view.get();
        }
    }

    /** Catches errors thrown by its children; errors thrown by its own fallback propagate upwards. */
    static final class ErrorBoundary implements Component {
        private final Component child;
        private final Function<RenderError, Component> fallback;
        RenderError error;

        ErrorBoundary(Component child, Function<RenderError, Component> fallback) {
            this.child = child;
            this.fallback = fallback;
        }

        public String render() {
            if (error == null) {
                try {
                    return child.render();
                } catch (RenderError e) {
                    error = e;
                }
            }
            return fallback.apply(error).render();
        }

        void reset() {
            error = null;
        }
    }

    final ErrorBoundary root;
    final ErrorBoundary shows;

    /** global boundary > RootLayout[header, shows boundary > page]. */
    ErrorBoundaryApp(Map<String, Integer> fails) {
        Flaky page = new Flaky(fails.getOrDefault("page", 0), "Failed to fetch shows", () -> "page");
        Flaky fallbackFails = new Flaky(fails.getOrDefault("fallback", 0), "Fallback failed", () -> "");
        shows = new ErrorBoundary(page, e -> () -> {
            fallbackFails.render(); // may throw -> caught by the global boundary
            return "shows-error(" + e.getMessage() + ")";
        });
        Flaky layout = new Flaky(fails.getOrDefault("layout", 0), "Root layout failed",
                () -> "root[header," + shows.render() + "]");
        root = new ErrorBoundary(layout, e -> () -> "global-error(" + e.getMessage() + ")");
    }

    /** Retry button: resets the boundary showing its fallback; a reset remounts everything below it. */
    boolean resetNearest() {
        if (root.error != null) {
            root.reset();
            shows.reset();
            return true;
        }
        if (shows.error != null) {
            shows.reset();
            return true;
        }
        return false;
    }
}
