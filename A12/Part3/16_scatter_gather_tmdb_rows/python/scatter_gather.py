"""Scatter-Gather: TMDB Row Scatter-Gather (Promise.all fan-out over row requests, all-or-nothing gather)."""
import asyncio


class Row:
    def __init__(self, key: str, ms: int, ok: bool, count: int) -> None:
        self.key, self.ms, self.ok, self.count = key, ms, ok, count


async def recipient(row: Row) -> dict:
    """One TMDB endpoint; latency is simulated (reported, not slept)."""
    await asyncio.sleep(0)
    return {"ok": row.ok, "ms": row.ms, "results": ["show"] * row.count}


async def fetch_rows(rows: list, error_message: str) -> dict:
    responses = await asyncio.gather(*(recipient(r) for r in rows))  # scatter, keeps request order
    elapsed = max((r["ms"] for r in responses), default=0)  # concurrent: slowest reply
    if any(not r["ok"] for r in responses):  # gather: completeness rule
        return {"error": error_message, "elapsed": elapsed}
    return {"rows": {row.key: len(r["results"]) for row, r in zip(rows, responses)}, "elapsed": elapsed}


def sequential_cost(rows: list) -> int:
    """What the same requests would cost one after another."""
    return sum(r.ms for r in rows)
