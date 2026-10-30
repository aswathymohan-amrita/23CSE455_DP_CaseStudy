"""Context Object: tRPC Request Context (createTRPCContext -> createInnerTRPCContext -> middleware refinement)."""
import re

DEFAULT_REGION = "US"
REGION_HEADERS = ("x-vercel-ip-country", "cf-ipcountry")
DEFAULT_MAX_PROFILES = 5
PLANS = {"u1": ("Premium", 3, 5), "u2": ("Mobile", 1, 2)}  # fake database: user -> (plan, tier, maxProfiles)


class TRPCError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def normalise_region(code) -> str:
    value = (code or "").strip().upper()
    return value if re.fullmatch(r"[A-Z]{2}", value) else DEFAULT_REGION


def region_from_headers(headers: dict) -> str:
    for name in REGION_HEADERS:
        if headers.get(name):
            return normalise_region(headers[name])
    return normalise_region(None)


def create_inner_context(session, region) -> dict:
    """Protocol-independent context (also used by tests without HTTP)."""
    return {"session": session, "db": PLANS, "region": normalise_region(region)}


def create_context(headers: dict) -> dict:
    """Per-request factory: extracts session and region from the HTTP request once."""
    return create_inner_context(headers.get("session"), region_from_headers(headers))


def enforce_user_is_authed(ctx: dict) -> dict:
    if not ctx["session"]:
        raise TRPCError("UNAUTHORIZED")
    return {**ctx, "session": ctx["session"]}  # narrowed copy, original untouched


def attach_subscription(ctx: dict) -> dict:
    plan = ctx["db"].get(ctx["session"])
    return {**ctx, "subscription": plan[0] if plan else None,
            "planTier": plan[1] if plan else 0, "maxProfiles": plan[2] if plan else DEFAULT_MAX_PROFILES}


PROCEDURES = {  # name -> (middlewares, resolver reading only ctx)
    "whoami": ((enforce_user_is_authed,), lambda ctx: ctx["session"]),
    "region": ((), lambda ctx: ctx["region"]),
    "plan": ((enforce_user_is_authed, attach_subscription),
             lambda ctx: f"tier={ctx['planTier']},max={ctx['maxProfiles']}"),
}


def call(name: str, ctx: dict) -> str:
    middlewares, resolver = PROCEDURES[name]
    for mw in middlewares:
        ctx = mw(ctx)
    return f"{resolver(ctx)};keys={','.join(sorted(ctx))}"
