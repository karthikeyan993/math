"""Independent Python copy of the formula grammar in docs/components/logic.ts.

Same rules: NOT applies to the single atom after it; one parenthesis level may
not mix binary operators or chain IMPLIES. Written separately (not generated
from the TS) so that tools/verify/components.py can cross-check the two.
"""

from __future__ import annotations

import itertools
import re

OPS = {"AND", "OR", "XOR", "IMPLIES", "IFF"}
TOKEN = re.compile(r"\(|\)|[A-Za-z_][A-Za-z0-9_]*")


def parse(src: str):
    if TOKEN.sub("", src).strip():
        raise ValueError(f"bad character in formula: {src}")
    toks = TOKEN.findall(src)
    pos = 0

    def atom():
        nonlocal pos
        if pos >= len(toks):
            raise ValueError(f"formula ends early: {src}")
        t = toks[pos]
        pos += 1
        if t == "NOT":
            return ("not", atom())
        if t == "(":
            e = level()
            if pos >= len(toks) or toks[pos] != ")":
                raise ValueError(f"missing ) in: {src}")
            pos += 1
            return e
        if t == ")" or t in OPS:
            raise ValueError(f"unexpected {t} in: {src}")
        return ("var", t)

    def level():
        nonlocal pos
        args = [atom()]
        op = None
        while pos < len(toks) and toks[pos] in OPS:
            nxt = toks[pos]
            pos += 1
            if op and nxt != op:
                raise ValueError(f"mixes {op} and {nxt} without parentheses: {src}")
            if nxt in ("IMPLIES", "IFF") and op:
                raise ValueError(f"chained {nxt} needs parentheses: {src}")
            op = nxt
            args.append(atom())
        return ("bin", op, args) if op else args[0]

    f = level()
    if pos != len(toks):
        raise ValueError(f"unexpected {toks[pos]} in: {src}")
    return f


def evaluate(f, env: dict[str, bool]) -> bool:
    kind = f[0]
    if kind == "var":
        return env[f[1]]
    if kind == "not":
        return not evaluate(f[1], env)
    _, op, args = f
    v = [evaluate(a, env) for a in args]
    if op == "AND":
        return all(v)
    if op == "OR":
        return any(v)
    if op == "XOR":
        return sum(v) % 2 == 1
    if op == "IFF":
        return v[0] == v[1]
    if op == "IMPLIES":
        return (not v[0]) or v[1]
    raise AssertionError(op)


def table(variables: list[str], columns: list[str]) -> list[str]:
    fs = [parse(c) for c in columns]
    out = []
    for f in fs:
        out.append("".join(
            "T" if evaluate(f, dict(zip(variables, r))) else "F"
            for r in itertools.product([True, False], repeat=len(variables))
        ))
    return out
