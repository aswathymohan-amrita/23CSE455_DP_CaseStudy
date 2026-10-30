"""Builder: tRPC Procedure Builder (immutable fluent builder; query()/mutation() build the product)."""


class TRPCError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code
        self.trace = []  # middlewares that ran before the call stopped


class Procedure:
    """Product: a frozen definition that can be called."""

    def __init__(self, kind: str, middlewares: tuple, resolver) -> None:
        self.kind = kind
        self.middlewares = middlewares
        self.resolver = resolver

    def call(self, user, raw):
        ctx = {"user": user, "input": raw}
        trace = []
        for name, mw in self.middlewares:
            trace.append(name)
            try:
                mw(ctx)  # raises TRPCError to stop the call
            except TRPCError as e:
                e.trace = trace
                raise
        return self.kind + ":" + self.resolver(ctx), trace


class ProcedureBuilder:
    """Every step returns a NEW builder; the receiver is never changed."""

    def __init__(self, middlewares: tuple = ()) -> None:
        self.middlewares = middlewares

    def use(self, name: str, mw) -> "ProcedureBuilder":
        return ProcedureBuilder(self.middlewares + ((name, mw),))

    def input(self, parser) -> "ProcedureBuilder":
        return self.use("input", parser)

    def query(self, resolver) -> Procedure:
        return Procedure("query", self.middlewares, resolver)

    def mutation(self, resolver) -> Procedure:
        return Procedure("mutation", self.middlewares, resolver)


def enforce_user_is_authed(ctx):
    if ctx["user"] is None:
        raise TRPCError("UNAUTHORIZED")


def string_input(ctx):
    if ctx["input"] is None:
        raise TRPCError("BAD_REQUEST")


def number_input(ctx):
    if ctx["input"] is None or not ctx["input"].lstrip("-").isdigit():
        raise TRPCError("BAD_REQUEST")
    ctx["input"] = str(int(ctx["input"]))


def no_op(ctx):
    pass


public_procedure = ProcedureBuilder()  # t.procedure
protected_procedure = public_procedure.use("auth", enforce_user_is_authed)
RESOLVERS = {
    "echo": lambda ctx: ctx["input"] if ctx["input"] is not None else "none",
    "whoami": lambda ctx: ctx["user"] or "anonymous",
}
STEPS = {
    "use:log": lambda b: b.use("log", no_op),
    "use:timing": lambda b: b.use("timing", no_op),
    "input:string": lambda b: b.input(string_input),
    "input:number": lambda b: b.input(number_input),
}


def build(steps: list):
    """Director: applies the step names in order to a base builder."""
    current = {"public": public_procedure, "protected": protected_procedure}[steps[0]]
    for step in steps[1:]:
        if isinstance(current, Procedure):
            raise TRPCError("ALREADY_BUILT")
        kind, _, name = step.partition(":")
        current = getattr(current, kind)(RESOLVERS[name]) if kind in ("query", "mutation") else STEPS[step](current)
    if not isinstance(current, Procedure):
        raise TRPCError("NOT_BUILT")
    return current
