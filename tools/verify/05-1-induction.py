"""Verify the numeric claims in docs/lessons/05-1-induction.md (MCS §5.1).

The formulas hold for all n, which these checks can't show: they are evidence.
The proofs are in the lesson.
"""

from _common import check, done

N = 2000
check("evidence: 1 + ... + n = n(n+1)/2 for n < 2000", all(sum(range(1, n + 1)) == n * (n + 1) // 2 for n in range(N)))
check("evidence: 1 + 3 + ... + (2n-1) = n^2 for n < 2000",
      all(sum(2 * k - 1 for k in range(1, n + 1)) == n * n for n in range(N)))
check("inductive-step algebra: n(n+1)/2 + (n+1) = (n+1)(n+2)/2 (agree at 4+ points, so identical)",
      all(n * (n + 1) + 2 * (n + 1) == (n + 1) * (n + 2) for n in range(-3, 3)))
check("odd step: n^2 + 2n + 1 = (n+1)^2 as polynomials", all(n * n + 2 * n + 1 == (n + 1) ** 2 for n in range(-3, 3)))
check("next odd number after 2n-1 is 2(n+1)-1 = 2n+1", all(2 * (n + 1) - 1 == 2 * n + 1 for n in range(100)))

# Courtyard: tiles T(0) = 0, T(n+1) = 4 T(n) + 1 (one tile in the centre, four quadrants).
T = [0]
for _ in range(10):
    T.append(4 * T[-1] + 1)
check("courtyard tile counts start 0, 1, 5, 21, 85", T[:5] == [0, 1, 5, 21, 85])
check("courtyard tiles = (4^n - 1)/3 for n <= 10", all(T[n] == (4**n - 1) // 3 and (4**n - 1) % 3 == 0 for n in range(11)))
check("tiles cover every square but Bill: 3 T(n) = 4^n - 1", all(3 * T[n] == 4**n - 1 for n in range(11)))

# Horses: with n + 1 = 2, "first n" and "last n" are disjoint; with n + 1 >= 3 they overlap.
check("horses: first n and last n of n+1 overlap iff n >= 2",
      all((len(set(range(n)) & set(range(1, n + 1))) > 0) == (n >= 2) for n in range(1, 50)))
check("student 17 is reached from student 0 by 17 uses of rule 2", len(range(0, 17)) == 17)

done()
