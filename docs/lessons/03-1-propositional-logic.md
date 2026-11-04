---
title: 3.1–3.3 Propositional logic
outline: deep
---

# 3.1–3.3 Propositional logic

<FocusTimer />

<div class="lesson-meta">

**Lecture:** 1 · Predicates, Sets, and Proofs ([OCW lecture videos](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/video_galleries/lecture-videos/)) · **Textbook:** MCS §3.1–3.3 (pp. 48–56) · **Time:** 3 short sittings of 10–20 min · **You'll need:** [1.1–1.7 Propositions and proofs](/lessons/01-proofs) (what a proposition is)

</div>

::: details The same operator in four notations (MCS §3.2.2, p. 54)
| Book (words) | Maths | C / Java / Rust | Python |
|---|---|---|---|
| NOT($P$) | $\neg P$ or $\overline{P}$ | `!p` | `not p` |
| $P$ AND $Q$ | $P \wedge Q$ | `p && q` | `p and q` |
| $P$ OR $Q$ | $P \vee Q$ | `p \|\| q` | `p or q` |
| $P$ XOR $Q$ | $P \oplus Q$ | `p ^ q` (on bools) | `p != q` |
| $P$ IMPLIES $Q$ | $P \rightarrow Q$ | `!p \|\| q` | `not p or q` |
| $P$ IFF $Q$ | $P \leftrightarrow Q$ | `p == q` | `p == q` |

There's no IMPLIES operator in C-family languages, so you write `!p || q`. Hold that thought until §3.
:::

## 1. Code review: can this condition be simpler?

This is from the book (MCS §3.2, p. 52):

```c
if (x > 0 || (x <= 0 && y > 100)) {
    ...
}
```

Let $A$ be "$x > 0$" and $B$ be "$y > 100$". Then `x <= 0` is NOT($A$), and the condition is $A$ OR (NOT($A$) AND $B$).

<EquivalenceChecker left="A OR (NOT(A) AND B)" right="A OR B" />

<Recall q="Explain in words why the x <= 0 check is redundant, without using the table.">

If $A$ is true, both sides are true, because the OR is already satisfied. If $A$ is false, then NOT($A$) is true, so the left side becomes just $B$, and so does the right. By the time `||` evaluates its right side, we already know $x \le 0$, so checking it again adds nothing. (This is the book's "reasoning by cases" on p. 53.)

</Recall>

A truth table checks **every** row. With 2 variables there are 4 rows, so the table above is a complete proof that the two conditions are equivalent, not just evidence. Compare that with $n^2 + n + 41$ in the last lesson, where there were infinitely many cases.

## 2. AND, OR, XOR: one trap

The only surprise is that **OR is inclusive**: $P$ OR $Q$ is true when both are true (MCS §3.1.1, p. 49). "You may have cake, or you may have ice cream" lets a mathematician have both. If you mean "exactly one", that's XOR. In code, `||` is OR, and XOR on bools is `!=`.

<TruthTable vars="P,Q" cols="P OR Q; P XOR Q" title="OR vs XOR: they differ in exactly one row">

They differ only in the first row, where both are true. OR says T there and XOR says F.

</TruthTable>

<Checkpoint :n="1" :of="3" next="§3–4, IMPLIES, the operator everyone gets wrong (about 20 min)" />

## 3. IMPLIES is a promise

Start with a puzzle, before any definition:

<WasonCards rule="If a card has a vowel on one side, then it has an even number on the other side." cards="A, K, 4, 7" answer="0,3">

Think of the rule as a **promise**: vowel $\Rightarrow$ even. A promise is broken only when the if-part happens and the then-part doesn't. So the only cards that can break it are a vowel with an odd number, or an odd number with a vowel.

- **A** (vowel): an odd number on the back would break the promise. **Turn it.**
- **K** (not a vowel): the promise says nothing about consonants. Whatever is on the back, the rule survives.
- **4** (even): the then-part is already true. A vowel or a consonant on the back is fine either way. This is a very common wrong pick.
- **7** (odd): if there's a vowel on the back, the promise is broken. **Turn it.**

</WasonCards>

Now the formal table. Fill it in using the promise idea: when is a promise broken?

<TruthTable vars="P,Q" cols="P IMPLIES Q" title="P IMPLIES Q">

It's false only in row 2: $P$ true, $Q$ false. The book's one-line summary is worth memorising:

> An implication is true exactly when the if-part is false or the then-part is true.
>
> <cite>MCS §3.1.3, p. 50</cite>

So in code, `P IMPLIES Q` is `!p || q`.

</TruthTable>

<Predict question="Rows 3 and 4 (P false) make the implication true whatever Q is. That feels like cheating. Why is it the right choice? Think of a system spec: 'if sensor 1 fires, take action 1; if sensor 2 fires, take action 2; …', for 12 sensors, and today only sensors 2 and 5 fired.">

The system obeys its spec when **all 12** rules hold, so the spec is rule 1 AND rule 2 AND … AND rule 12 (MCS p. 51). Today only sensors 2 and 5 fired, and the system took actions 2 and 5. It behaved perfectly. For the spec to come out true, the other 10 rules, whose sensors **didn't fire**, have to count as true. A promise that wasn't triggered can't have been broken.

You've met this before: $\emptyset \subseteq B$ is true, and in Python `all([])` is `True`. A rule that has nothing to check passes.

</Predict>

So "If pigs fly, then your account won't get hacked" is mathematically **true**, because pigs don't fly (MCS p. 50). Mathematical implication ignores cause and effect. That's what makes it simple enough to compute with.

## 4. Contrapositive vs converse

Three versions of "if hungry, then grumpy" (MCS §3.3.1, pp. 54–55), with $P$ = hungry and $Q$ = grumpy:

<TruthTable vars="P,Q" cols="P IMPLIES Q; NOT(Q) IMPLIES NOT(P); Q IMPLIES P" title="Original, contrapositive, converse">

Columns 1 and 2 match on every row, so **an implication and its contrapositive are equivalent**. Column 3, the converse, differs in rows 2 and 3, so **the converse is a different claim**.

Back to the cards: turning over the **7** was checking the contrapositive ("not even $\Rightarrow$ not a vowel").

</TruthTable>

<EquivalenceChecker left="(P IMPLIES Q) AND (Q IMPLIES P)" right="P IFF Q" />

That's why proving an "iff" means proving both directions (§1.6 in the last lesson).

<Checkpoint :n="2" :of="3" next="§5–7, valid vs satisfiable, SAT and short-circuit evaluation (about 15 min)" />

## 5. Valid, satisfiable, and why SAT is hard

> A *valid* formula is one which is always true, no matter what truth values its variables may have.
>
> <cite>MCS §3.3.2, p. 56</cite>

> A *satisfiable* formula is one which can sometimes be true—that is, there is some assignment of truth values to its variables that makes it true.
>
> <cite>MCS §3.3.2, p. 56</cite>

In truth-table terms: **valid** means every row is T, and **satisfiable** means at least one row is T. "$F$ and $G$ are equivalent" is the same as "$F$ IFF $G$ is valid".

<Recall q="Fill in the blank, and say why: 'P is satisfiable iff NOT(P) is not ____.'">

**Valid.** "$P$ is true in some row" means the same as "NOT($P$) is false in some row", which means "NOT($P$) is not true in every row". (MCS p. 56)

</Recall>

<Predict question="Checking satisfiability with a truth table takes 2ⁿ rows for n variables. Roughly how many rows for 30 variables? For 300?">

$2^{30} = 1{,}073{,}741{,}824$, about a billion. A laptop can manage that. $2^{300}$ is about $10^{90}$, far more than the number of atoms in the observable universe (about $10^{80}$). No one knows a fundamentally faster method that works for every formula. Whether one exists is the **P vs NP** problem, the biggest open question in theoretical CS (MCS §3.5, p. 63).

</Predict>

::: info Where you'll meet SAT
Package managers have to pick versions that satisfy every "A needs B ≥ 2", "B conflicts with C" constraint at once. Some of them do this with a SAT solver: Fedora's `dnf` and openSUSE's `zypper` use `libsolv`, which is built on one. The rules are a big AND of implications, exactly like the sensor spec in §3. "Can these packages be installed together?" is the question "is this formula satisfiable?". Real formulas have thousands of variables. SAT solvers often succeed anyway, but there's no guarantee (MCS p. 63).
:::

## 6. Equivalent, but not interchangeable in C

$A$ AND $B$ is equivalent to $B$ AND $A$, which a 4-row table proves. Now look at this:

```c
if (p != NULL && p->len > 0) { ... }   // version 1
if (p->len > 0 && p != NULL) { ... }   // version 2
```

<Predict question="The two conditions are logically equivalent. Are the two lines of code equivalent? What happens when p is NULL?">

No. C evaluates `&&` left to right and **stops early** once the result is known. In version 1, when `p` is `NULL`, the left side is false, so `p->len` is never evaluated. In version 2, `p->len` runs first and dereferences a null pointer, which is undefined behaviour and usually a crash.

Logical equivalence is about **truth values**. Code also has **evaluation order and side effects**, which truth tables can't see. When you use a logical law to rewrite real code, check that nothing on either side can crash or change state.

</Predict>

## 7. Spot the bug

<Predict question="A student writes: 'The contrapositive of “if n² is even, then n is even” is “if n² is odd, then n is odd.”' Is that the contrapositive? If not, what is it, and is it equivalent to the original?">

It isn't the contrapositive. The student negated both sides but **didn't swap them**. That form, NOT($P$) IMPLIES NOT($Q$), is called the *inverse*, and it's equivalent to the **converse** ($Q$ IMPLIES $P$), not to the original. (Check it: put `NOT(P) IMPLIES NOT(Q)` and `Q IMPLIES P` into the equivalence checker above.) The real contrapositive negates **and swaps**: "if $n$ is odd, then $n^2$ is odd."

</Predict>

## Check yourself

<Recall q="When is P IMPLIES Q false? Write it as code.">

Only when $P$ is true and $Q$ is false. In code: `!p || q`.

</Recall>

<Recall q="Which is equivalent to P IMPLIES Q: its converse or its contrapositive? Write both.">

The contrapositive, NOT($Q$) IMPLIES NOT($P$), is equivalent. The converse, $Q$ IMPLIES $P$, is not.

</Recall>

<Recall q="Valid vs satisfiable in terms of truth-table rows.">

Valid means every row is T. Satisfiable means at least one row is T.

</Recall>

<Recall q="Why is a truth table a proof, while 40 passing tests of n² + n + 41 weren't?">

A truth table covers every possible assignment, because there are only finitely many. The tests covered a finite part of an infinite set.

</Recall>

<Checkpoint :n="3" :of="3" />

---

**Next:** [3.6 Quantifiers](/lessons/03-6-quantifiers), the last part of the Lecture 1 reading.

**Problems** (separate sitting): **Problem 3.1** (p. 68) and **Problem 3.10** (p. 76). Add `flashcards/03-1-propositional-logic.csv` to Anki. Part 2 of `python3 lab/01-logic.py` has you write your own truth-table checker.
