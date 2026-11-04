"""Shared helpers for the per-lesson verification scripts.

Each script in tools/verify/ re-checks, by brute force, every numeric or finite
claim its lesson makes. Run one with `python3 tools/verify/<lesson>.py`, or run
them all through `python3 tools/check_content.py`.

A passing check on a finite claim (a truth table, a small domain) is a proof.
A passing check on an infinite claim (all n, all reals) is only evidence, and
the scripts label those checks "evidence".
"""

from __future__ import annotations

import itertools
import sys
from typing import Callable, Iterable

_failures: list[str] = []
_count = 0


def check(name: str, ok: bool) -> None:
    """Record one claim. Prints only failures; `done()` prints the summary."""
    global _count
    _count += 1
    if not ok:
        _failures.append(name)
        print(f"FAIL: {name}")


def done() -> None:
    script = sys.argv[0]
    if _failures:
        print(f"{script}: {len(_failures)} of {_count} claims FAILED")
        sys.exit(1)
    print(f"{script}: all {_count} claims verified")


def rows(n: int) -> Iterable[tuple[bool, ...]]:
    """Truth-table rows in textbook order: T before F, first variable slowest."""
    return itertools.product([True, False], repeat=n)


def equivalent(f: Callable[..., bool], g: Callable[..., bool], n: int) -> bool:
    return all(f(*r) == g(*r) for r in rows(n))


def valid(f: Callable[..., bool], n: int) -> bool:
    return all(f(*r) for r in rows(n))


def satisfiable(f: Callable[..., bool], n: int) -> bool:
    return any(f(*r) for r in rows(n))


def implies(p: bool, q: bool) -> bool:
    return (not p) or q


def iff(p: bool, q: bool) -> bool:
    return p == q


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def all_unary_predicates(domain: list) -> Iterable[dict]:
    """Every possible predicate P on `domain`, as a dict x -> bool."""
    for bits in itertools.product([False, True], repeat=len(domain)):
        yield dict(zip(domain, bits))


def all_binary_predicates(domain: list) -> Iterable[dict]:
    """Every possible predicate P(x, y) on `domain`, as a dict (x, y) -> bool."""
    pairs = [(x, y) for x in domain for y in domain]
    for bits in itertools.product([False, True], repeat=len(pairs)):
        yield dict(zip(pairs, bits))
