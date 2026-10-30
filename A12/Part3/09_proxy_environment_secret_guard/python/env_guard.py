"""Proxy (protection): Environment Secret Guard."""


class EnvGuard:
    """Proxy: attribute reads (env.NAME) are checked, then forwarded to the real variables."""

    def __init__(self, real: dict, is_server: bool, production: bool) -> None:
        object.__setattr__(self, "_real", real)
        object.__setattr__(self, "_is_server", is_server)
        object.__setattr__(self, "_production", production)

    def __getattr__(self, name: str):
        if not object.__getattribute__(self, "_is_server") and not name.startswith("NEXT_PUBLIC_"):
            if object.__getattribute__(self, "_production"):
                raise PermissionError("Attempted to access a server-side environment variable on the client")
            raise PermissionError(f"Attempted to access server-side environment variable '{name}' on the client")
        return object.__getattribute__(self, "_real").get(name)
