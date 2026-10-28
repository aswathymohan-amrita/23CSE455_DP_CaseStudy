"""Read text from saved provider events using the selected function."""

from __future__ import annotations

import json
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def stream_claude(events: list[dict[str, Any]]) -> Iterator[str]:
    for event in events:
        delta = event.get("delta")
        if event.get("type") == "content_block_delta" and isinstance(delta, dict):
            text = delta.get("text") if delta.get("type") == "text_delta" else None
            if isinstance(text, str) and text:
                yield text


def stream_openai(events: list[dict[str, Any]]) -> Iterator[str]:
    for event in events:
        choices = event.get("choices")
        if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
            continue
        delta = choices[0].get("delta")
        text = delta.get("content") if isinstance(delta, dict) else None
        if isinstance(text, str) and text:
            yield text


def stream_gemini(events: list[dict[str, Any]]) -> Iterator[str]:
    for event in events:
        text = event.get("text")
        if isinstance(text, str) and text:
            yield text


STRATEGIES = {
    "claude": stream_claude,
    "openai": stream_openai,
    "gemini": stream_gemini,
}


def run(input_data: Any) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        return {"error": "input must be an object"}
    provider = input_data.get("provider")
    if not isinstance(provider, str):
        return {"error": "provider must be a string"}
    strategy = STRATEGIES.get(provider)
    if strategy is None:
        return {"error": f"Unsupported provider: {provider}"}
    events = input_data.get("events")
    if not isinstance(events, list):
        return {"error": "events must be an array"}
    if any(not isinstance(event, dict) for event in events):
        return {"error": "each event must be an object"}
    chunks = list(strategy(events))
    return {"chunks": chunks, "text": "".join(chunks)}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python implementation.py INPUT_JSON")
    with Path(sys.argv[1]).open(encoding="utf-8") as source:
        print(json.dumps(run(json.load(source)), ensure_ascii=False))
