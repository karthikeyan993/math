"""Verify every finite claim in docs/lessons/03-6-quantifiers.md (MCS §3.6).

Claims over small finite domains are proved by exhaustion. Claims about R or Z
are checked on samples and labelled "evidence".
"""

import itertools
import math
import sqlite3
from fractions import Fraction

from _common import all_binary_predicates, all_unary_predicates, check, done, implies

D = range(5)

# --- §1 game statements -----------------------------------------------------
check("forall x exists y. x + y = 4 is true on D, with y = 4 - x in D",
      all((4 - x) in D and x + (4 - x) == 4 for x in D))
check("exists y forall x. x + y = 4 is false on D", not any(all(x + y == 4 for x in D) for y in D))
check("forall x exists y. y > x is false on D (x = 4)", not all(any(y > x for y in D) for x in D)
      and not any(y > 4 for y in D))
check("evidence: forall x exists y. y > x holds on N (y = x + 1), sampled to 10^4",
      all(x + 1 > x for x in range(10_000)))
check("exists y forall x. y >= x is true on D (y = 4)", all(4 >= x for x in D))

# --- §2 all()/any() lines and the book's R examples ---------------------------
check("all(x*x >= 0 for x in range(5)) is True", all(x * x >= 0 for x in range(5)))
check("any(5x^2 - 7 == 0 for x in range(5)) is False", not any(5 * x * x - 7 == 0 for x in range(5)))
check("x = sqrt(7/5) solves 5x^2 - 7 = 0 (exact: x^2 = 7/5)", 5 * Fraction(7, 5) - 7 == 0)
check("float sanity: 5*sqrt(7/5)^2 - 7 ~ 0", abs(5 * math.sqrt(7 / 5) ** 2 - 7) < 1e-12)
check("x = 0 is a counterexample to forall x. 5x^2 - 7 = 0", 5 * 0 * 0 - 7 != 0)
check("evidence: x^2 >= 0 on a grid of reals", all((Fraction(k, 7)) ** 2 >= 0 for k in range(-700, 701)))

# --- §3 order of quantifiers ------------------------------------------------
def AxEy(P, dom): return all(any(P[(x, y)] for y in dom) for x in dom)
def EyAx(P, dom): return any(all(P[(x, y)] for x in dom) for y in dom)

for n in (1, 2, 3):
    dom = list(range(n))
    preds = list(all_binary_predicates(dom))
    check(f"(3.27) exists y forall x => forall x exists y: valid on every P over |D| = {n} ({len(preds)} predicates)",
          all(implies(EyAx(P, dom), AxEy(P, dom)) for P in preds))
diag = {(x, y): x == y for x in D for y in D}
check("diagonal x = y on D is a counter-model: AxEy true, EyAx false", AxEy(diag, D) and not EyAx(diag, D))
W = range(-30, 31)
check("evidence (book's counter-model on Z, window): every y has a bigger x (x = y + 1)", all((y + 1) > y for y in W))
check("no x is bigger than every y: y = x is always a counterexample", all(not (x > x) for x in W))

# Hash tables: universe U of keys, m slots, |U| > m >= 2.
for u, m in [(3, 2), (4, 2), (4, 3), (5, 3)]:
    U = range(u)
    hs = list(itertools.product(range(m), repeat=u))  # every function U -> slots
    sets = [S for k in range(m + 1) for S in itertools.combinations(U, k)]  # all S with |S| <= m
    no_coll = lambda h, S: len({h[k] for k in S}) == len(S)
    check(f"hash |U|={u}, m={m}: forall S exists h with no collisions", all(any(no_coll(h, S) for h in hs) for S in sets))
    check(f"hash |U|={u}, m={m}: NOT exists h forall S (every h has a colliding pair)",
          not any(all(no_coll(h, S) for S in sets) for h in hs))

# Goldbach swap: no single p + q equals both 4 and 6.
check("exists p, q forall n. n = p + q is false: 4 != 6", 4 != 6)

# --- §4 negation ------------------------------------------------------------
for n in (1, 2, 3, 4):
    dom = list(range(n))
    check(f"(3.22) NOT forall = exists NOT, every unary P on |D| = {n}",
          all((not all(P[x] for x in dom)) == any(not P[x] for x in dom) for P in all_unary_predicates(dom)))
    check(f"(3.23) NOT exists = forall NOT, every unary P on |D| = {n}",
          all((not any(P[x] for x in dom)) == all(not P[x] for x in dom) for P in all_unary_predicates(dom)))
for n in (1, 2, 3):
    dom = list(range(n))
    check(f"NOT(forall x exists y P) == exists x forall y NOT P, every binary P on |D| = {n}",
          all((not AxEy(P, dom)) == any(all(not P[(x, y)] for y in dom) for x in dom) for P in all_binary_predicates(dom)))
check("worked example on D: exists x forall y. y <= x is true with x = 4", all(y <= 4 for y in D))
check("faded example on D: forall y exists x. x + y != 4 is true", all(any(x + y != 4 for x in D) for y in D))
check("not all(...) == any(not ...) on a sample", (not all([True, False, True])) == any(not v for v in [True, False, True]))

# SQL: students who took every course, via double NOT EXISTS, vs Python all().
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE students(id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE courses(id INTEGER PRIMARY KEY);
CREATE TABLE enrolled(student INTEGER, course INTEGER);
INSERT INTO students VALUES (1,'ada'),(2,'bob'),(3,'cy');
INSERT INTO courses VALUES (10),(11),(12);
INSERT INTO enrolled VALUES (1,10),(1,11),(1,12),(2,10),(2,12),(3,11);
""")
QUERY = """SELECT s.name FROM students s
WHERE NOT EXISTS (
  SELECT 1 FROM courses c
  WHERE NOT EXISTS (
    SELECT 1 FROM enrolled e WHERE e.student = s.id AND e.course = c.id));"""
sql = sorted(r[0] for r in db.execute(QUERY))
took = set(db.execute("SELECT student, course FROM enrolled"))
students = list(db.execute("SELECT id, name FROM students"))
courses = [r[0] for r in db.execute("SELECT id FROM courses")]
py = sorted(name for sid, name in students if all((sid, c) in took for c in courses))
check(f"SQL double NOT EXISTS == Python all(): {sql}", sql == py == ["ada"])

done()
