# Mistake ledger

Mistakes are logged like bugs. The tutor uses this file to aim your quizzes at your own error patterns.

**Root-cause tags:** `hypothesis-unstated` · `base-case` · `step-not-all-n` · `circular` · `quantifier` · `algebra` · `definition` · `edge-case` · `wrong-technique` · `notation`

| Date | Where | Symptom | Root cause | Fix / lesson |
|---|---|---|---|---|
| 2026-11-04 | Prereq Q2: factor $k^3 + 3k^2 + 2k$ | Stuck; only knew how to factor quadratics | `algebra` | Pull out the common factor first: $k(k^2+3k+2) = k(k+1)(k+2)$ |
| 2026-11-04 | Prereq Q4: $2^{k+1} - 2^k$ | Answered $2$ (likely did $2^{(k+1)-k}$) | `algebra` | You subtract exponents when you *divide* powers, not when you subtract them. Factor: $2^k(2-1) = 2^k$. Sanity-check with $k = 3$ |
| 2026-11-04 | Prereq Q5: $\log_2(8x)$ given $\log_2 x = 5$ | Answered $40$ (multiplied) | `definition` | Logs not known yet. Rebuild from scratch before Lecture 5 (answer: $3 + 5 = 8$) |
| 2026-11-04 | Prereq Q7: $A - B$ | Gave the symmetric difference $\{1,2,5\}$ | `notation` | $A - B$ = in $A$ and not in $B$ (MCS §4.1.2, p. 105). It is not symmetric: $B - A \ne A - B$ |
| 2026-11-04 | Prereq Q8: $\{3\} \in \{1,2,3\}$ | Said true | `definition` | $\in$ asks "is this thing one of the elements?" A `Set<int>` isn't one of the ints. Use $\subseteq$ for "every element is in" |
| 2026-11-04 | Prereq Q8: $\emptyset \subseteq \{1,2,3\}$ | Said false | `quantifier` | Vacuous truth: there's no counterexample, so it's true. Same as Python's `all([]) == True` |
| 2026-11-04 | Prereq Q10: $\forall x\, \exists y.\ y > x$ | Said false ("we don't know $x$") | `quantifier` | It's a game: $\forall$ = opponent picks, $\exists$ = you pick after seeing earlier picks. Win with $y = x + 1$. The order of quantifiers changes the meaning |
