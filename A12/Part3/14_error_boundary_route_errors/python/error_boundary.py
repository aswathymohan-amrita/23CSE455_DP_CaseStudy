"""Error Boundary: Shows Segment Error Boundary + Root Global Error Boundary (Next.js error.tsx / global-error.tsx)."""


class RenderError(Exception):
    pass


class Flaky:
    """A component that throws for its first `fails` renders (simulates TMDB/layout failures)."""

    def __init__(self, fails: int, message: str, view) -> None:
        self.fails, self.message, self.view, self.renders = fails, message, view, 0

    def render(self) -> str:
        self.renders += 1
        if self.renders <= self.fails:
            raise RenderError(self.message)
        return self.view()


class ErrorBoundary:
    """Catches errors thrown by its children; errors thrown by its own fallback propagate upwards."""

    def __init__(self, child, fallback) -> None:
        self.child, self.fallback, self.error = child, fallback, None

    def render(self) -> str:
        if self.error is None:
            try:
                return self.child.render()
            except RenderError as e:
                self.error = e
        return self.fallback(self.error).render()

    def reset(self) -> None:
        self.error = None


def build_app(fails: dict):
    """global boundary > RootLayout[header, shows boundary > page]."""
    page = Flaky(fails.get("page", 0), "Failed to fetch shows", lambda: "page")
    fallback_fails = Flaky(fails.get("fallback", 0), "Fallback failed", lambda: "")
    shows = ErrorBoundary(page, lambda e: Flaky(0, "", lambda: _shows_error(fallback_fails, e)))
    layout = Flaky(fails.get("layout", 0), "Root layout failed", lambda: f"root[header,{shows.render()}]")
    root = ErrorBoundary(layout, lambda e: Flaky(0, "", lambda: f"global-error({e})"))
    return root, shows


def _shows_error(fallback: Flaky, error: RenderError) -> str:
    fallback.render()  # may throw -> caught by the global boundary
    return f"shows-error({error})"


def reset_nearest(root: ErrorBoundary, shows: ErrorBoundary) -> bool:
    """Retry button: resets the boundary that is showing its fallback; a reset remounts the subtree,
    so boundaries below it start without an error as well."""
    if root.error is not None:
        root.reset()
        shows.reset()
        return True
    if shows.error is not None:
        shows.reset()
        return True
    return False
