"""Front Controller: tRPC API Front Controller (/api/trpc/[trpc] -> createNextApiHandler -> appRouter)."""


class TRPCError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class Procedure:
    """A command registered in the router: protected? input required? resolver(ctx, input)."""

    def __init__(self, resolver, protected: bool = True, needs_input: bool = False) -> None:
        self.resolver = resolver
        self.protected = protected
        self.needs_input = needs_input


def _list_resolver(ctx, value):
    if value == "boom":
        raise RuntimeError("database unavailable")
    return f"list({value})"


def app_router() -> dict:
    """Command registry: dotted procedure path -> Procedure (state after CH01)."""
    return {
        "user.getCurrent": Procedure(lambda ctx, _: f"user({ctx['user']})"),
        "profile.getAll": Procedure(lambda ctx, _: f"profiles({ctx['user']})"),
        "profile.getOne": Procedure(lambda ctx, v: f"profile({v})", needs_input=True),
        "icon.getAll": Procedure(lambda ctx, _: "icons", protected=False),
        "myList.getAll": Procedure(_list_resolver, needs_input=True),
        "catalogue.checkAccess": Procedure(lambda ctx, v: f"access({v})", needs_input=True),
    }


class FrontController:
    """Single entry point: shared context creation, dispatch by path, one error policy."""

    def __init__(self, router: dict, create_context, on_error) -> None:
        self.router = router
        self.create_context = create_context
        self.on_error = on_error

    def handle(self, user, path):
        if path is None:  # route file not named [trpc]: no path, nothing dispatched
            return ["ERROR:INTERNAL_SERVER_ERROR"]
        ctx = self.create_context(user)  # once per HTTP request, shared by a batch
        return [self._dispatch(call, ctx) for call in path.split(",")]

    def _dispatch(self, call: str, ctx: dict) -> str:
        name, _, value = call.partition("=")
        try:
            proc = self.router.get(name)
            if proc is None:
                raise TRPCError("NOT_FOUND")
            if proc.protected and ctx["user"] is None:
                raise TRPCError("UNAUTHORIZED")
            if proc.needs_input and not value:
                raise TRPCError("BAD_REQUEST")
            return "OK:" + proc.resolver(ctx, value or None)
        except TRPCError as e:
            self.on_error(name, e.code)
            return "ERROR:" + e.code
        except Exception:  # resolver bug -> generic server error
            self.on_error(name, "INTERNAL_SERVER_ERROR")
            return "ERROR:INTERNAL_SERVER_ERROR"
