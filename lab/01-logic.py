"""Conjecture lab for Lecture 1: MCS §1.1–1.7, §3.1–3.3, §3.6.

Work top to bottom. Each part: compute, look, guess, test. Then go prove it.
Remember: a passing check over an INFINITE set is evidence, not proof.
A check over EVERY case of a FINITE set is a proof.
"""

import itertools

# --- Part 1: a pattern that lies (MCS §1.1) -----------------------------------
def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, int(n**0.5) + 1))

p = lambda n: n * n + n + 41
fails = [n for n in range(100) if not is_prime(p(n))]
print("Part 1: n < 100 where n^2 + n + 41 is NOT prime:", fails)
# TODO: look at the list. Which of these are multiples of 41? Predict which
# others will appear, then explain p(41) and p(82) without a calculator.
# TODO: try your own polynomial, e.g. n^2 - n + 41 or n^2 + n + 17.
# How long does its prime streak last?
print()


# --- Part 2: your own truth-table checker (MCS §3.2–3.3) ------------------------
def rows(n: int):
    """All 2^n truth assignments, in textbook order (T before F)."""
    return itertools.product([True, False], repeat=n)


def equivalent(f, g, n: int) -> bool:
    return None  # TODO: True iff f(*r) == g(*r) for every row r in rows(n)


def valid(f, n: int) -> bool:
    return None  # TODO


def satisfiable(f, n: int) -> bool:
    return None  # TODO


implies = lambda p, q: (not p) or q
if equivalent(lambda a, b: a, lambda a, b: a, 2) is None:
    print("Part 2: fill in equivalent / valid / satisfiable, then rerun.\n")
else:
    print("Part 2:")
    print("  contrapositive equivalent?", equivalent(lambda p, q: implies(p, q), lambda p, q: implies(not q, not p), 2))
    print("  converse equivalent?      ", equivalent(lambda p, q: implies(p, q), lambda p, q: implies(q, p), 2))
    print("  P OR NOT P valid?         ", valid(lambda p: p or not p, 1))
    # TODO: guess first, then test: is (P IMPLIES Q) OR (Q IMPLIES P) valid?
    # TODO: is P IMPLIES (Q IMPLIES P) valid? Explain the result in words.
    # TODO (bonus): Python's `<=` on bools. Is `p <= q` the same as implies(p, q)?
    print()


# --- Part 3: quantifiers are all() and any() (MCS §3.6) -------------------------
D = range(5)
print("Part 3, over D = {0, ..., 4}:")
print("  forall x exists y. x + y = 4 :", all(any(x + y == 4 for y in D) for x in D))
print("  exists y forall x. x + y = 4 :", any(all(x + y == 4 for x in D) for y in D))
# TODO: predict, then compute, each of these over D. Then say which ones would
# change if D were all of N:
#   forall x exists y. y > x
#   exists x forall y. x <= y
#   forall x exists y. x * y == 0
#   exists y forall x. x * y == 0
# TODO: write the negation of "forall x exists y. y > x" with the NOT pushed all
# the way in, and check that it has the opposite truth value on D.
print()


# --- Part 4: how big must the party be? (MCS §1.7) ------------------------------
def has_club_or_strangers(n: int, met: dict) -> bool:
    """met[(i, j)] for i < j says whether i and j have met."""
    return any(met[(a, b)] == met[(a, c)] == met[(b, c)] for a, b, c in itertools.combinations(range(n), 3))


def always_true(n: int) -> bool:
    pairs = list(itertools.combinations(range(n), 2))
    return all(has_club_or_strangers(n, dict(zip(pairs, bits)))
               for bits in itertools.product([False, True], repeat=len(pairs)))


print("Part 4: does every party of n people contain a club of 3 or 3 strangers?")
for n in range(3, 7):
    print(f"  n = {n}: {always_true(n)}")
# TODO: why is the n = 6 result a PROOF, but Part 1's 40 passing tests weren't?
# TODO (hard): how many ways can 6 people meet? Predict 2^? before computing it.
# How many of the 5-person patterns are counterexamples? Predict, then count.
