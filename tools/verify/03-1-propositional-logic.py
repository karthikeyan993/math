"""Verify every finite claim in docs/lessons/03-1-propositional-logic.md (MCS §3.1–3.3).

Everything here is over finitely many truth assignments, so each passing check
is a proof, not just evidence (except the integer sampling in §1, labelled).
"""

import itertools

from _common import check, done, equivalent, iff, implies, rows, satisfiable, valid
import _logic

T = lambda vars_, cols: _logic.table(vars_, cols)

# --- §1 the code-review condition (MCS §3.2, pp. 52–53) ---------------------
check("A OR (NOT A AND B) is equivalent to A OR B",
      equivalent(lambda A, B: A or ((not A) and B), lambda A, B: A or B, 2))
check("evidence: same result on real ints, x in -50..50, y in 50..150",
      all((x > 0 or (x <= 0 and y > 100)) == (x > 0 or y > 100) for x in range(-50, 51) for y in range(50, 151)))
check("x <= 0 is exactly NOT(x > 0) on the sampled ints", all((x <= 0) == (not x > 0) for x in range(-50, 51)))

# --- §2 OR vs XOR -----------------------------------------------------------
or_, xor = T(["P", "Q"], ["P OR Q", "P XOR Q"])
check("OR and XOR differ only in row 1 (both true)", [i + 1 for i in range(4) if or_[i] != xor[i]] == [1])
check("Python: p != q is XOR on bools", all((p != q) == ((p or q) and not (p and q)) for p, q in rows(2)))
check("C/Rust/Java ^ on 0/1 values is XOR", all(((int(p) ^ int(q)) == 1) == (p != q) for p, q in rows(2)))

# --- §3 IMPLIES (MCS §3.1.3, p. 50) -----------------------------------------
check("P IMPLIES Q is F only in row 2 (P=T, Q=F)", T(["P", "Q"], ["P IMPLIES Q"]) == ["TFTT"])
check("P IMPLIES Q == (not p) or q", all(implies(p, q) == ((not p) or q) for p, q in rows(2)))

# Wason cards: a card must be turned iff some possible hidden side breaks
# "vowel on one side => even number on the other".
def breaks(letter_is_vowel, number_is_even):
    return letter_is_vowel and not number_is_even
cards = [("letter", True), ("letter", False), ("number", True), ("number", False)]  # A, K, 4, 7
must = [i for i, (kind, val) in enumerate(cards)
        if any(breaks(val, hidden) if kind == "letter" else breaks(hidden, val) for hidden in (True, False))]
check("Wason: exactly cards A and 7 (indices 0, 3) must be turned", must == [0, 3])

# Sensor spec (MCS p. 51): 12 rules C_i IMPLIES A_i; only C2, C5 fire, A2, A5 taken.
C = {i: i in (2, 5) for i in range(1, 13)}
A = {i: i in (2, 5) for i in range(1, 13)}
check("spec (3.1) is true when only C2, C5 fire and A2, A5 are taken", all(implies(C[i], A[i]) for i in C))
check("10 of the 12 rules are true only because their hypothesis is false",
      sum(1 for i in C if not C[i]) == 10)
check("Python: all([]) is True (vacuous truth)", all([]) is True)

# --- §4 contrapositive vs converse (MCS §3.3.1, pp. 54–55) ------------------
orig, contra, conv = T(["P", "Q"], ["P IMPLIES Q", "NOT(Q) IMPLIES NOT(P)", "Q IMPLIES P"])
check("implication == contrapositive on every row", orig == contra)
check("converse differs exactly in rows 2 and 3", [i + 1 for i in range(4) if orig[i] != conv[i]] == [2, 3])
check("(P IMPLIES Q) AND (Q IMPLIES P) is equivalent to P IFF Q",
      equivalent(lambda P, Q: implies(P, Q) and implies(Q, P), iff, 2))

# --- §5 validity and satisfiability (MCS §3.3.2, p. 56) ---------------------
check("P OR NOT(P) is valid", valid(lambda P: P or not P, 1))
check("[(P->Q) AND (Q->R)] -> (P->R) is valid",
      valid(lambda P, Q, R: implies(implies(P, Q) and implies(Q, R), implies(P, R)), 3))
# Over ALL truth functions of 2 and 3 variables:
for n in (2, 3):
    funcs = list(itertools.product([True, False], repeat=2**n))
    as_fn = lambda bits: (lambda *r: bits[list(rows(n)).index(r)])
    check(f"F satisfiable iff NOT F not valid (all {len(funcs)} functions of {n} vars)",
          all(satisfiable(as_fn(b), n) == (not valid(lambda *r, b=b: not as_fn(b)(*r), n)) for b in funcs))
funcs2 = list(itertools.product([True, False], repeat=4))
fn = lambda bits: (lambda *r: bits[list(rows(2)).index(r)])
check("F, G equivalent iff (F IFF G) valid (all 16 x 16 pairs of 2-var functions)",
      all(equivalent(fn(f), fn(g), 2) == valid(lambda P, Q, f=f, g=g: fn(f)(P, Q) == fn(g)(P, Q), 2)
          for f in funcs2 for g in funcs2))
check("2^30 = 1,073,741,824", 2**30 == 1_073_741_824)
check("2^300 is about 10^90 (between 10^90 and 10^91)", 10**90 < 2**300 < 10**91)

# --- §6 short-circuit: AND is commutative on truth values ------------------
check("A AND B is equivalent to B AND A", equivalent(lambda A, B: A and B, lambda A, B: B and A, 2))

# --- §7 inverse == converse, inverse != original ---------------------------
inv, = T(["P", "Q"], ["NOT(P) IMPLIES NOT(Q)"])
check("inverse NOT(P) IMPLIES NOT(Q) is equivalent to the converse", inv == conv)
check("inverse is NOT equivalent to the original", inv != orig)

done()
