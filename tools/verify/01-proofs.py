"""Verify every numeric/finite claim in docs/lessons/01-proofs.md (MCS §1.1–1.7)."""

import itertools
from fractions import Fraction

from _common import check, done, implies, is_prime, rows

# --- §1 Hook: p(n) = n^2 + n + 41 (MCS §1.1, p. 5) -------------------------
p = lambda n: n * n + n + 41
check("p(0) = 41", p(0) == 41)
check("p(1), p(2), p(3), p(20) = 43, 47, 53, 461", [p(1), p(2), p(3), p(20)] == [43, 47, 53, 461])
check("p(n) prime for every 0 <= n <= 39", all(is_prime(p(n)) for n in range(40)))
check("p(39) = 1601", p(39) == 1601)
check("p(40) = 1681 = 41 * 41, not prime", p(40) == 1681 == 41 * 41 and not is_prime(p(40)))
check("n = 40 is the FIRST n with p(n) not prime", next(n for n in range(100) if not is_prime(p(n))) == 40)
check("p(41) = 41 * 43", p(41) == 41 * 43)
check("PrimeStreak: after n = 40, more failures turn up below 60",
      len([n for n in range(41, 60) if not is_prime(p(n))]) >= 2)

# Euler's conjecture counterexample (MCS §1.1, p. 6): exact integer arithmetic.
a, b, c, d = 95800, 217519, 414560, 422481
check("Elkies: 95800^4 + 217519^4 + 414560^4 = 422481^4", a**4 + b**4 + c**4 == d**4)

# --- §3 Inference rules (MCS §1.4.1, p. 10) ---------------------------------
# A rule is sound iff every assignment making all antecedents true makes the
# consequent true. Two variables -> 4 assignments, so these checks are proofs.
def sound(antecedents, consequent):
    return all(consequent(P, Q, R) for P, Q, R in rows(3) if all(f(P, Q, R) for f in antecedents))

def counterexamples(antecedents, consequent):
    return sorted({(P, Q) for P, Q, R in rows(3)
                   if all(f(P, Q, R) for f in antecedents) and not consequent(P, Q, R)}, reverse=True)

check("modus ponens is sound",
      sound([lambda P, Q, R: P, lambda P, Q, R: implies(P, Q)], lambda P, Q, R: Q))
check("P->Q, Q->R / P->R is sound",
      sound([lambda P, Q, R: implies(P, Q), lambda P, Q, R: implies(Q, R)], lambda P, Q, R: implies(P, R)))
check("NOT P -> NOT Q / Q -> P is sound",
      sound([lambda P, Q, R: implies(not P, not Q)], lambda P, Q, R: implies(Q, P)))
non_rule = ([lambda P, Q, R: implies(not P, not Q)], lambda P, Q, R: implies(P, Q))
check("NOT P -> NOT Q / P -> Q is NOT sound", not sound(*non_rule))
check("its only counterexample is P = T, Q = F", counterexamples(*non_rule) == [(True, False)])
# "Affirming the consequent", used in the lesson's spot-the-bug.
affirm = ([lambda P, Q, R: Q, lambda P, Q, R: implies(P, Q)], lambda P, Q, R: P)
check("Q, P -> Q / P is NOT sound", not sound(*affirm))
check("its only counterexample is P = F, Q = T", counterexamples(*affirm) == [(False, True)])

# --- §4 Theorem 1.5.1 (MCS p. 12): -x^3 + 4x + 1 > 0 for 0 <= x <= 2 ----------
# Two polynomials of degree <= 3 that agree at 4+ points are identical, so this
# exact check at 6 integer points PROVES the factorisation.
check("-x^3 + 4x = x(2 - x)(2 + x) as polynomials",
      all(-x**3 + 4 * x == x * (2 - x) * (2 + x) for x in range(-3, 3)))
check("at x = 1: 4x = 4 and x^3 = 1", (4 * 1, 1**3) == (4, 1))
check("evidence: -x^3 + 4x + 1 > 0 on a 2001-point grid of [0, 2]",
      all(-x**3 + 4 * x + 1 > 0 for x in (Fraction(k, 1000) for k in range(2001))))
check("outside the hypothesis it fails: x = 3 gives -14", -(3**3) + 4 * 3 + 1 == -14)
# FactorSigns messages: "all three factors >= 0" is exactly the band [0, 2];
# with one negative factor the total can go below 0 (on both sides of the band);
# with two negative factors (x < -2) the product is positive.
f = lambda x: -x**3 + 4 * x + 1
grid = [Fraction(k, 100) for k in range(-300, 301)]
check("x >= 0, 2 - x >= 0, 2 + x >= 0 all hold exactly when 0 <= x <= 2",
      all((x >= 0 and 2 - x >= 0 and 2 + x >= 0) == (0 <= x <= 2) for x in grid))
check("one negative factor, total < 0 somewhere in (-2, 0)", any(f(x) < 0 for x in grid if -2 < x < 0))
check("one negative factor, total < 0 somewhere in (2, 3]", any(f(x) < 0 for x in grid if 2 < x <= 3))
check("two negative factors only when x < -2, and then the product is > 0",
      all((sum(v < 0 for v in (x, 2 - x, 2 + x)) == 2) == (x < -2) for x in grid)
      and all(x * (2 - x) * (2 + x) > 0 for x in grid if x < -2))
check("never three negative factors", all(sum(v < 0 for v in (x, 2 - x, 2 + x)) < 3 for x in grid))

# --- §5 Theorem 1.6.1 (MCS p. 14): standard deviation examples ---------------
def std_squared(xs):
    mu = Fraction(sum(xs), len(xs))
    return sum((x - mu) ** 2 for x in xs) / len(xs)

check("scores 7, 7, 7: standard deviation 0", std_squared([7, 7, 7]) == 0)
check("scores 6, 8: mean 7, standard deviation 1", Fraction(6 + 8, 2) == 7 and std_squared([6, 8]) == 1)

# --- §6 Proof by cases (MCS §1.7, pp. 15–16): 6 people ----------------------
def has_club_or_strangers(n, met):
    return any(met[frozenset((i, j))] == met[frozenset((i, k))] == met[frozenset((j, k))]
               for i, j, k in itertools.combinations(range(n), 3))

def all_groups(n):
    pairs = [frozenset(e) for e in itertools.combinations(range(n), 2)]
    for bits in itertools.product([False, True], repeat=len(pairs)):
        yield dict(zip(pairs, bits))

check("all 2^15 ways 6 people can have met contain a club of 3 or 3 strangers",
      all(has_club_or_strangers(6, g) for g in all_groups(6)))
bad5 = [g for g in all_groups(5) if not has_club_or_strangers(5, g)]
check("with 5 people the theorem fails (counterexamples exist)", len(bad5) > 0)
pentagon = {frozenset((i, j)): (j - i) % 5 in (1, 4) for i, j in itertools.combinations(range(5), 2)}
check("the pentagon (each person met exactly their 2 neighbours) is a counterexample",
      not has_club_or_strangers(5, pentagon))
check("every 5-person counterexample is a pentagon: 12 of them, each person met exactly 2",
      len(bad5) == 12 and all(sum(g[frozenset((v, u))] for u in range(5) if u != v) == 2
                             for g in bad5 for v in range(5)))
check("the two cases cover everything: of 5 others, >= 3 met x or >= 3 did not",
      all(k >= 3 or 5 - k >= 3 for k in range(6)))
from math import comb
check("6 people have C(6,2) = 15 pairs and 2^15 = 32,768 configurations", comb(6, 2) == 15 and 2**15 == 32768)

# --- §3 TruthTable in the lesson: the non-rule's counterexample is row 2 -----
import _logic
ante, concl = _logic.table(["P", "Q"], ["NOT(P) IMPLIES NOT(Q)", "P IMPLIES Q"])
check("non-rule table: only row 2 (P=T, Q=F) has antecedent T and conclusion F",
      [i + 1 for i in range(4) if ante[i] == "T" and concl[i] == "F"] == [2])

done()
