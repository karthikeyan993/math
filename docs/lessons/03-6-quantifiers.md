---
title: 3.6 Quantifiers
outline: deep
---

# 3.6 Quantifiers

<FocusTimer />

<div class="lesson-meta">

**Lecture:** 1 · Predicates, Sets, and Proofs ([OCW lecture videos](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/video_galleries/lecture-videos/)) · **Textbook:** MCS §3.6 (pp. 63–68) · **Time:** 3 short sittings of 10–20 min · **You'll need:** [3.1–3.3 Propositional logic](/lessons/03-1-propositional-logic) (NOT, IMPLIES)

</div>

::: details Notation refresher
| Symbol | Read it as | Python, over a finite domain `D` |
|---|---|---|
| $\forall x \in D.\ P(x)$ | "for all $x$ in $D$, $P(x)$" | `all(P(x) for x in D)` |
| $\exists x \in D.\ P(x)$ | "there is an $x$ in $D$ with $P(x)$" | `any(P(x) for x in D)` |
| $\forall x\, \exists y.\ P(x, y)$ | "for every $x$ there is a $y$ (which may depend on $x$)…" | `all(any(P(x, y) for y in D) for x in D)` |
| $\mathbb{R}$ | the real numbers | |
:::

## 1. Play first

Quantifiers are a game between you and an opponent. Read the statement left to right. At each $\forall$ the opponent picks a value, trying to make you lose. At each $\exists$ **you** pick, and you can see everything picked so far. The statement is true exactly when you can always win.

<QuantifierGame />

<Predict question="Statements 1 and 2 use the same predicate, x + y = 4. Only the order of the quantifiers differs. In one sentence, why does the order change who wins?">

In $\forall x\, \exists y$ you pick $y$ **after** seeing $x$, so $y$ can depend on $x$ (take $y = 4 - x$). In $\exists y\, \forall x$ you have to commit to one $y$ **before** seeing $x$, and that one $y$ has to work for every $x$. A later picker can react to everything picked before.

</Predict>

## 2. ∀ is `all()`, ∃ is `any()`

On a finite domain, a quantifier is just a loop:

```python
D = range(5)
all(x * x >= 0 for x in D)              # ∀x ∈ D. x² ≥ 0
any(5 * x * x - 7 == 0 for x in D)      # ∃x ∈ D. 5x² − 7 = 0   (False on this D)
```

The book's examples are over $\mathbb{R}$ (MCS §3.6.1, p. 63). $\forall x \in \mathbb{R}.\ x^2 \ge 0$ is true. $\exists x \in \mathbb{R}.\ 5x^2 - 7 = 0$ is true, with witness $x = \sqrt{7/5}$. $\forall x \in \mathbb{R}.\ 5x^2 - 7 = 0$ is false; try $x = 0$. Over $\mathbb{R}$ you can't run the loop, so you need a proof. That's the whole reason we're here.

<Predict question="'If you can solve any problem we come up with, then you get an A.' Is 'any' a ∀ or an ∃ here? Write both readings.">

It's ambiguous, and the book uses this very example (MCS p. 64):

- $(\forall x \in \text{Probs}.\ \text{Solves}(x))$ IMPLIES $G$: you must solve **every** problem.
- $(\exists x \in \text{Probs}.\ \text{Solves}(x))$ IMPLIES $G$: solving **one** is enough.

English "any" can mean either. When you write specs or proofs, use "every" or "some", never "any".

</Predict>

<Checkpoint :n="1" :of="3" next="§3, order of quantifiers, with a picture (about 15 min)" />

## 3. Order matters: rows and columns

Draw a predicate $P(x, y)$ as a grid, with a dot wherever it's true. Then every two-quantifier statement is a simple visual check:

<QuantifierGrid />

<Recall q="Using the grid: why does ∃y ∀x imply ∀x ∃y? (One full column does what for the rows?)">

A full column puts a dot in **every row**, so every row has a dot. In general, if one $y$ works for all $x$, then for each $x$ you can pick that same $y$. The book explains this as formula (3.27) (MCS §3.6.6, p. 67).

</Recall>

<Recall q="And why does ∀x ∃y NOT imply ∃y ∀x? Name a grid that shows it.">

Load **x = y**, the diagonal. Every row has a dot, but no column is full. A grid like this, where the hypothesis is true and the conclusion false, is a **counter-model** (MCS p. 68). The book's own counter-model uses the integers with $P(x, y) ::= x > y$. For every $y$ there's a bigger $x$, but no $x$ is bigger than every $y$.

</Recall>

::: info Where CS uses this: hash tables
Say there are more possible keys than slots in your table.

- **"For every set of keys, there is a hash function with no collisions on it."** This is $\forall S\, \exists h$, and it's **true**: once you've seen the keys, you can assign them distinct slots (as long as there are at most as many keys as slots).
- **"There is one hash function with no collisions on every set of keys."** This is $\exists h\, \forall S$, and it's **false**. There are more keys than slots, so any fixed $h$ sends two keys to the same slot (pigeonhole), and the set containing just those two collides.

The false one is the game with the opponent moving last: you fix $h$, then an attacker who knows $h$ picks keys that collide. That's a real attack (hash flooding), and it's why Python has randomised its string hash per process by default since 3.3. The attacker no longer knows $h$ when choosing keys.

`tools/verify/03-6-quantifiers.py` brute-forces both claims on small universes.
:::

The book's own example of a swap that breaks the meaning is Goldbach's Conjecture (MCS §3.6.3, p. 65):

$$\forall n \in \text{Evens}\ \exists p \in \text{Primes}\ \exists q \in \text{Primes}.\ n = p + q$$

<Predict question="Move the ∀n to the end: ∃p ∃q ∀n. n = p + q. What does this say, and is it true?">

It says there are two primes whose sum is **every** even number greater than 2 at once. That's obviously false: $4$ and $6$ can't both equal the same $p + q$. Goldbach's actual statement (the original order) is still unsolved.

</Predict>

<Checkpoint :n="2" :of="3" next="§4–5, negating quantifiers and the final check (about 15 min)" />

## 4. Negation: push the NOT through, flip each quantifier

"Not everyone likes ice cream" means "someone doesn't like ice cream" (MCS §3.6.5, p. 66):

$$\text{NOT}(\forall x.\ P(x)) \iff \exists x.\ \text{NOT}(P(x)) \qquad \text{NOT}(\exists x.\ P(x)) \iff \forall x.\ \text{NOT}(P(x))$$

In Python, `not all(...)` is `any(not ...)`. On the grid, "not every row has a dot" means "some row is empty".

Worked example. Negate $\forall x\, \exists y.\ y > x$:

$$\begin{aligned}
\text{NOT}(\forall x\, \exists y.\ y > x) &\iff \exists x.\ \text{NOT}(\exists y.\ y > x) \\
&\iff \exists x\, \forall y.\ \text{NOT}(y > x) \\
&\iff \exists x\, \forall y.\ y \le x
\end{aligned}$$

<Recall q="Self-explain: what rule justifies each of the three lines?">

Line 1: NOT($\forall$) becomes $\exists$ NOT. Line 2: NOT($\exists$) becomes $\forall$ NOT. Line 3: NOT($y > x$) is $y \le x$. Each step moves the NOT one place to the right and flips the quantifier it passes. Over $D = \{0, \dots, 4\}$ the result is true with $x = 4$, which matches statement 3 of the game being false.

</Recall>

<Recall q="Your turn (faded): negate ∃y ∀x. x + y = 4, and push the NOT all the way in.">

$\forall y\, \exists x.\ x + y \neq 4$. "Whatever $y$ you commit to, the opponent can find an $x$ that misses." That's exactly how the opponent beats you in game statement 2.

</Recall>

::: info Where CS uses this: SQL has no FOR ALL
SQL has `EXISTS` but no "for all", so you write $\forall$ as NOT $\exists$ NOT. "Students who have taken **every** course" becomes "students for whom there is **no** course they have **not** taken":

```sql
SELECT s.name FROM students s
WHERE NOT EXISTS (
  SELECT 1 FROM courses c
  WHERE NOT EXISTS (
    SELECT 1 FROM enrolled e WHERE e.student = s.id AND e.course = c.id));
```

That's $\forall c.\ \text{Took}(s, c)$ rewritten as $\text{NOT}(\exists c.\ \text{NOT}\ \text{Took}(s, c))$. `tools/verify/03-6-quantifiers.py` runs this query in SQLite and checks it against Python's `all()`.
:::

## 5. Spot the bug

<Predict question="Claim: 'The negation of “every request gets a response within 1 s” is “every request takes longer than 1 s.”' What's wrong, and what's the correct negation?">

The quantifier didn't flip. Negating $\forall r.\ \text{Fast}(r)$ gives $\exists r.\ \text{NOT}(\text{Fast}(r))$: **at least one** request takes longer than 1 s. That's what an SLO violation alert fires on. You need one counterexample, not all of them.

</Predict>

## Check yourself

<Recall q="In ∀x ∃y. P(x, y), can y depend on x? What about in ∃y ∀x. P(x, y)?">

In $\forall x\, \exists y$, yes: $y$ is picked after $x$. In $\exists y\, \forall x$, no: one $y$ has to work for every $x$.

</Recall>

<Recall q="Which implication between them is valid?">

$\exists y\, \forall x \implies \forall x\, \exists y$. One full column gives every row a dot. The reverse fails; the diagonal is a counter-model.

</Recall>

<Recall q="Negate ∀x ∃y. P(x, y).">

$\exists x\, \forall y.\ \text{NOT}(P(x, y))$.

</Recall>

<Recall q="Which technique proves a quantified formula is NOT valid?">

Give a counter-model: a domain and an interpretation of the predicate that make it false.

</Recall>

<Checkpoint :n="3" :of="3" />

---

**This finishes the Lecture 1 reading.** Next up is Lecture 2 and [5.1 Ordinary induction](/lessons/05-1-induction). Lecture 2 also assigns §1.8–1.9 and §4.1, which don't have lessons here yet.

**Problems** (separate sitting): **Problem 3.26** (p. 87, which statements are false over $\mathbb{N}$, $\mathbb{Z}$ and $\mathbb{R}$) and **Problem 3.27** (p. 87, which formulas say "no student has been on a quiz show"). Add `flashcards/03-6-quantifiers.csv` to Anki. Part 3 of `python3 lab/01-logic.py` uses `all`/`any` to test quantified claims.
