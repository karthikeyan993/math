---
title: 1.1–1.7 Propositions and proofs
outline: deep
---

# 1.1–1.7 Propositions and proofs

<FocusTimer />

<div class="lesson-meta">

**Lecture:** 1 · Predicates, Sets, and Proofs ([OCW lecture videos](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/video_galleries/lecture-videos/)) · **Textbook:** MCS §1.1–1.7 (pp. 5–16) · **Time:** 4 short sittings of 10–20 min · **You'll need:** high-school algebra.

</div>

::: details Notation refresher (open if any symbol is rusty)
| Symbol | Read it as | Example |
|---|---|---|
| $\mathbb{N}$ | the nonnegative integers $0, 1, 2, \dots$ | $0 \in \mathbb{N}$ |
| $\mathbb{Z}^+$ | the positive integers $1, 2, 3, \dots$ | $0 \notin \mathbb{Z}^+$ |
| $\forall$ | "for all" | $\forall n \in \mathbb{N}.\ n \ge 0$ |
| $::=$ | "equals, by definition" | $p(n) ::= n^2 + n + 41$ |
| $\blacksquare$ | "end of proof" (also QED) | |
:::

## 1. Your tests passed. Are you done?

Here's a claim: for every $n \in \mathbb{N}$, the number $p(n) = n^2 + n + 41$ is prime. You're the QA engineer. Bet first, then run the tests.

<PrimeStreak />

<Recall q="Without a calculator: why is p(40) obviously divisible by 41? (Use the trick from the prerequisites diagnostic: factor out the common factor.)">

$40^2 + 40 = 40(40 + 1) = 40 \cdot 41$. So $p(40) = 40 \cdot 41 + 41 = 41 \cdot 41$. In the same way, $p(41) = 41^2 + 41 + 41 = 41 \cdot 43$.

</Recall>

Forty passing tests in a row, and the claim is still false. The book's lesson is that you can't check a claim about an infinite set by checking a finite sample, however large (MCS §1.1, p. 6). This isn't a party trick: Euler conjectured in 1769 that $a^4 + b^4 + c^4 = d^4$ has no solution in positive integers. Nobody found one for **218 years**. Then Noam Elkies found

$$95800^4 + 217519^4 + 414560^4 = 422481^4.$$

(Big-integer check in `tools/verify/01-proofs.py`: it's exact.)

::: info Why this matters for you
A test suite is a finite sample of inputs. Tests are evidence; a proof covers **every** input at once. This course is about writing that second kind of argument.
:::

## 2. Propositions and predicates are just types

> A *proposition* is a statement (communication) that is either true or false.
>
> <cite>MCS §1.1, p. 5</cite>

> A *predicate* can be understood as a proposition whose truth depends on the value of one or more variables.
>
> <cite>MCS §1.2, p. 8</cite>

If you think in types, it's simple:

| Thing | Type | Example |
|---|---|---|
| proposition | `bool` (a value) | $2 + 3 = 5$ is `True`, $1 + 1 = 3$ is `False` |
| predicate | `Callable[[int], bool]` | $P(n) ::=$ "$n$ is a perfect square". $P(4)$ is `True`, $P(5)$ is `False` |
| ordinary function | `Callable[[int], int]` | $p(n) = n^2 + n + 41$, which gives a number |

The book warns that $P(n)$ and $p(n)$ look the same on paper (MCS §1.2, p. 8). With the type in mind you won't mix them up: you can ask whether $P(5)$ is true, but asking whether $p(5)$ is true is a type error.

<Predict question="Which of these are propositions (bool values)? (a) x > 3. (b) 7 is prime. (c) Is 7 prime? (d) Every even integer greater than 2 is the sum of two primes.">

- **(a)** No. It's a predicate, since it still needs an $x$.
- **(b)** Yes, and it's true.
- **(c)** No. A question isn't true or false.
- **(d)** Yes, even though **nobody knows which value it has**. This is Goldbach's Conjecture, open since 1742 (MCS §1.1, p. 7). A `bool` you haven't computed yet is still a `bool`.

</Predict>

<Checkpoint :n="1" :of="4" next="§3–4, what a proof is allowed to do, and proving 'if P then Q' (about 15 min)" />

## 3. A proof is a program that only uses sound steps

> A *proof* is a sequence of logical deductions from axioms and previously proved statements that concludes with the proposition in question.
>
> <cite>MCS §1.3, p. 9</cite>

Think of a proof as a program. The **axioms** are the standard library. In this book that means all the familiar facts from high-school maths (MCS §1.4, p. 9). The **inference rules** are the instructions, and an instruction is only allowed if it's **sound**:

> an assignment of truth values to the letters P, Q, …, that makes all the antecedents true must also make the consequent true.
>
> <cite>MCS §1.4.1, p. 10</cite>

In other words, a sound rule can never turn true inputs into a false output. The classic sound rule is **modus ponens**: from $P$ and "$P$ IMPLIES $Q$", conclude $Q$.

You'll need one fact from §3.1 (MCS p. 50): **$P$ IMPLIES $Q$ is false only when $P$ is true and $Q$ is false.** Now test the rule "from NOT($P$) IMPLIES NOT($Q$), conclude $P$ IMPLIES $Q$". Fill in both columns, then look for a row that is a counterexample: the antecedent is T and the conclusion is F.

<TruthTable vars="P,Q" cols="NOT(P) IMPLIES NOT(Q); P IMPLIES Q" title="Antecedent vs conclusion">

Row 2 ($P$ = T, $Q$ = F) breaks it: the antecedent is true but the conclusion is false. One bad row is enough to make the rule unsound. The book calls it a *non-rule* (MCS §1.4.1, p. 10).

</TruthTable>

## 4. Proving "if P, then Q"

**Method 1** (MCS §1.5.1, p. 11): write "Assume $P$", then show that $Q$ follows.

**Theorem 1.5.1** (MCS p. 12). If $0 \le x \le 2$, then $-x^3 + 4x + 1 > 0$.

Before reading any proof, play with it. Try to make the curve go negative:

<FactorSigns />

<Predict question="From the picture: what's the one algebraic fact that makes the proof work inside the band?">

Inside the band, all three factors of $-x^3 + 4x = x(2 - x)(2 + x)$ are $\ge 0$. A product of nonnegative numbers is nonnegative. Add $1$, and the result is $\ge 1 > 0$. That's the whole proof.

</Predict>

::: info Proof (MCS p. 12)
Assume $0 \le x \le 2$. Then $x$, $2 - x$ and $2 + x$ are all nonnegative, so their product is nonnegative. Adding $1$ gives a positive number:
$$x(2 - x)(2 + x) + 1 > 0.$$
Multiplying out the left side gives $-x^3 + 4x + 1 > 0$. $\blacksquare$
:::

<Recall q="Check the factorisation yourself: multiply out x(2 − x)(2 + x).">

$(2 - x)(2 + x) = 4 - x^2$ (difference of squares), so $x(4 - x^2) = 4x - x^3$. ✓

</Recall>

Notice what the book did. It did messy **scratchwork** to find the factorisation, and then wrote a clean proof. It's like debugging in a scratch file and then committing a clean diff. Keep the two separate.

**Method 2, the contrapositive** (MCS §1.5.2, p. 13). "$P$ IMPLIES $Q$" says exactly the same as "NOT($Q$) IMPLIES NOT($P$)". When the negations are easier to work with, prove that version instead.

::: info This is how you already debug
The claim "if the config is valid, the service starts" has the contrapositive "if the service didn't start, the config wasn't valid". These two say the same thing. Its **converse**, "if the service started, the config was valid", is a *different* claim and can be false: a bad config might still let the service start. §3.3 proves all of this with truth tables.
:::

<Recall q="Theorem 1.5.2 says: 'If r is irrational, then √r is irrational.' Write the contrapositive. Then prove it in two lines. (A number is rational if it equals m/n for some integers m, n.)">

Contrapositive: "if $\sqrt{r}$ is rational, then $r$ is rational."

Proof: say $\sqrt{r} = m/n$ with $m, n$ integers and $n \neq 0$. Squaring gives $r = m^2/n^2$, which is a ratio of integers, so $r$ is rational. $\blacksquare$ (MCS p. 13)

Notice how much easier "rational" (there *is* an $m/n$) is to work with than "irrational" (there is *no* $m/n$).

</Recall>

<Checkpoint :n="2" :of="4" next="§5–6, 'iff' and the party puzzle (about 20 min)" />

## 5. "If and only if" means two proofs (or one careful chain)

"$P$ IFF $Q$" means "$P$ IMPLIES $Q$" **and** "$Q$ IMPLIES $P$" (MCS §1.6.1, p. 14). Either prove the two directions separately, or build a **chain of iffs** where every link holds in both directions.

The book's chain (Theorem 1.6.1, p. 14): *the standard deviation of a list of scores is $0$ iff every score equals the mean $\mu$.*

$$\sqrt{\tfrac{\sum_i (x_i-\mu)^2}{n}} = 0 \iff \sum_i (x_i-\mu)^2 = 0 \iff \text{every } (x_i-\mu)^2 = 0 \iff \text{every } x_i = \mu$$

<Recall q="Self-explain the middle link: why is 'the sum of the squares is 0' equivalent to 'every square is 0'?">

Every square is $\ge 0$. A sum of nonnegative terms is $0$ exactly when every term is $0$: if one term were positive, the sum would be positive. In the other direction, a sum of zeros is $0$. Both directions hold.

</Recall>

<Predict question="Find the broken link: 'x = 2 ⟺ x² = 4 ⟺ x² − 4 = 0.'">

The first link. $x = 2 \implies x^2 = 4$ holds, but the reverse doesn't: $x = -2$ gives $x^2 = 4$. An iff chain is only as strong as its weakest link, so test every link **backwards** too.

</Predict>

## 6. Proof by cases: the party puzzle

**Theorem** (MCS §1.7, p. 15). Any 6 people include either 3 who have all met each other (a *club*) or 3 who have never met each other (*strangers*).

Don't take it on trust. Try to beat it:

<PartyGraph />

<Predict question="You probably found a 5-person counterexample but couldn't make one for 6. Before reading the proof: pick one person at the 6-person party. They have 5 lines. What can you say for sure about the colours of those 5 lines?">

At least 3 of them are the same colour. If at most 2 were green and at most 2 were red, there would be at most 4 lines, but there are 5. The whole proof starts here.

</Predict>

The book's proof (MCS pp. 15–16) picks a person $x$ and splits into two cases:

- **Case 1:** at least 3 people have met $x$. If any two of those 3 have met each other, then those two and $x$ are a club. If no two of them have met, the 3 are strangers.
- **Case 2:** at least 3 people have *not* met $x$. This is the same argument with the colours swapped.

> Part of a case analysis argument is showing that you've covered all the cases.
>
> <cite>MCS §1.7, p. 15</cite>

The prediction you just made is exactly that coverage argument.

::: info Two CS connections that are real
**Exhaustive matching.** Rust's `match` won't compile unless the arms cover every possible value. That's the "covered all the cases" duty from the quote above, enforced by a compiler.

**Proof by brute force is still proof.** The 6 people have $\binom{6}{2} = 15$ pairs, so there are $2^{15} = 32{,}768$ ways the meetings can go. A program can check them all, and `tools/verify/01-proofs.py` does: every one has a club or 3 strangers. A finite check over *every* case is a complete proof. (That's roughly how the Four Color Theorem was first proved, with a computer, MCS §1.1, p. 7.) Checking $n = 0$ to $39$ for $n^2 + n + 41$ wasn't a proof, because $\mathbb{N}$ has no last case.
:::

<Checkpoint :n="3" :of="4" next="§7 and the final check (about 10 min)" />

## 7. Spot the bug

<Predict question="'If my function is correct, all its tests pass. All its tests pass. Therefore my function is correct.' Write this as an inference rule. Is it sound?">

The rule is: from $Q$ and "$P$ IMPLIES $Q$", conclude $P$. **Not sound.** Take $P$ = F (the function is wrong) and $Q$ = T (the tests pass anyway): both antecedents are true and the conclusion is false. That's §1 again. This fallacy is called *affirming the consequent*. Modus ponens goes **forward** from $P$; this rule tries to go backward from $Q$.

</Predict>

## Check yourself

<Recall q="Proposition vs predicate, in one line each, using types.">

A proposition is a `bool`. A predicate is a function to `bool`, and it becomes a proposition once you give it arguments.

</Recall>

<Recall q="What makes an inference rule sound?">

Every assignment of truth values that makes all the antecedents true also makes the consequent true. It can't turn true inputs into a false output.

</Recall>

<Recall q="To prove 'if P then Q' by contrapositive, what do you assume and what do you show?">

Assume NOT($Q$), and show NOT($P$).

</Recall>

<Recall q="Why is checking all 32,768 party configurations a proof, while checking n = 0 to 39 isn't?">

The party has finitely many cases, and the check covers all of them. $\mathbb{N}$ has infinitely many, so any check leaves some out (and here $n = 40$ fails).

</Recall>

<Checkpoint :n="4" :of="4" />

---

**Next:** the second half of the Lecture 1 reading, [3.1–3.3 Propositional logic](/lessons/03-1-propositional-logic).

**Problems** (separate sitting, by hand): **Problem 1.7** (p. 24, prove $\max(r,s) + \min(r,s) = r + s$ by cases), **Problem 1.9** (p. 24, $|r + s| \le |r| + |s|$ by cases), **Problem 1.8** (p. 24, can an irrational number raised to an irrational power be rational?). Then ask the tutor to check your proofs. Optional: run `python3 lab/01-logic.py`, and add `flashcards/01-proofs.csv` to Anki.
