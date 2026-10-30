"""Locate a participant's line span in a source tree from an anchor regex.

span(root, file, anchor) -> "a-b" (1-based, inclusive) or "a" for one line.
The span starts at the first line matching `anchor` and ends at the first later line
where the bracket balance ((, {, [ minus ), }, ]) is back to zero and the line does
not end in a continuation token (=, ??, ||, &&, =>, ',', '(', '{', '[', ':' or '?').
Brackets inside string literals (template literals may span lines) and // comments
are ignored; a line ending in '}),' or '},' closes a property value; a next line
starting with '.', '?' or ':' continues a chain/ternary. `through` gives an explicit
end-line regex instead.
"""
import re

CONT = ("=", "??", "||", "&&", "=>", ",", "(", "{", "[", ":", "?")


def _strip(line, q=None):
    """Return (code without strings/comments, open quote carried to next line)."""
    out, i = [], 0
    while i < len(line):
        ch = line[i]
        if q:
            if ch == "\\":
                i += 2
                continue
            if ch == q:
                q = None
        elif ch in "\"'`":
            q = ch
        elif line.startswith("//", i):
            break
        else:
            out.append(ch)
        i += 1
    # only template literals may continue on the next line
    return "".join(out), (q if q == "`" else None)


def span(root, path, anchor, through=None):
    lines = open(f"{root}/{path}", encoding="utf-8").read().split("\n")
    rx = re.compile(anchor)
    start = next((i for i, l in enumerate(lines) if rx.search(l)), None)
    if start is None:
        raise LookupError(f"anchor {anchor!r} not found in {path}")
    if through:  # explicit end anchor
        end_rx = re.compile(through)
        end = next((j for j in range(start, len(lines)) if end_rx.search(lines[j])), None)
        if end is None:
            raise LookupError(f"end anchor {through!r} not found in {path}")
        return f"{start + 1}-{end + 1}"
    bal, q = 0, None
    for j in range(start, len(lines)):
        code, q = _strip(lines[j], q)
        bal += sum(code.count(c) for c in "({[") - sum(code.count(c) for c in ")}]")
        tail = code.rstrip()
        # "})," / "}," close a property value: the trailing comma is not a continuation
        closes_property = tail.endswith(",") and tail[:-1].rstrip().endswith((")", "}", "]"))
        nxt = next((l.strip() for l in lines[j + 1:] if l.strip()), "")
        if (bal <= 0 and q is None and (closes_property or not tail.endswith(CONT))
                and not nxt.startswith((".", "?", ":"))):  # chain / ternary continues
            return f"{start + 1}" if j == start else f"{start + 1}-{j + 1}"
    raise LookupError(f"unbalanced span for {anchor!r} in {path}")
