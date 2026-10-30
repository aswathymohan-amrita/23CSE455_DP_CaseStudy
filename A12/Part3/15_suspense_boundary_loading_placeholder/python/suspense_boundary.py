"""Suspense Boundary: Shows Loading Placeholder ((shows)/loading.tsx as the Suspense fallback of async pages)."""


class Pending(Exception):
    """Thrown by a child that is still waiting for data (React's suspend signal)."""


class FetchError(Exception):
    pass


class Dependency:
    def __init__(self, name: str, ms: int, fails: bool) -> None:
        self.name, self.ms, self.fails = name, ms, fails


class AsyncPage:
    """Async server page: awaits all its fetches (Promise.all) before it can render."""

    def __init__(self, deps: list) -> None:
        self.deps = deps

    def render(self, t: int) -> str:
        if any(d.ms > t for d in self.deps):
            raise Pending()
        failed = next((d for d in self.deps if d.fails), None)
        if failed:
            raise FetchError(failed.name)
        return f"page(rows={len(self.deps)})"


class SuspenseBoundary:
    """Renders the fallback while the child suspends; other errors pass through."""

    def __init__(self, child, fallback) -> None:
        self.child, self.fallback = child, fallback

    def render(self, t: int) -> str:
        try:
            return self.child.render(t)
        except Pending:
            return self.fallback()


def segment(page: AsyncPage, has_loading: bool):
    """Next.js LoadingBoundary: Suspense only if the segment has loading.tsx."""
    return SuspenseBoundary(page, lambda: "loading") if has_loading else page


def stream(root, deps: list) -> list:
    """Server streaming: render at every point in time where something can change; emit changed frames."""
    frames, last = [], None
    for t in sorted({0, *(d.ms for d in deps)}):
        try:
            view = root.render(t)
        except Pending:  # no boundary: nothing can be sent yet
            continue
        except FetchError as e:  # handled by the segment error boundary
            view = f"error({e})"
        if view != last:
            frames.append(f"t={t}:{view}")
            last = view
        if view != "loading":  # final frame sent
            break
    return frames
