---
title: 5.1 Ordinary induction
outline: deep
---

# 5.1 Ordinary induction

<FocusTimer />

<div class="lesson-meta">

**Textbook:** MCS §5.1 (pp. 137–146) · **Time:** 4 short sittings of 10–20 min, with checkpoints between them · **You'll need:** what a predicate $P(n)$ is (a statement that is true or false for each number $n$)

</div>

::: details Notation refresher (open if any symbol is rusty)
| Symbol | Read it as | Example |
|---|---|---|
| $\mathbb{N}$ | the nonnegative integers $0, 1, 2, \dots$ | $5 \in \mathbb{N}$ |
| $P(n)$ | "the claim, for this particular $n$" | $P(3)$: "$1+2+3 = 3\cdot4/2$" |
| $\forall n$ | "for every $n$" | $\forall n \in \mathbb{N}.\ n \ge 0$ |
| $A \implies B$ | "if $A$ is true then $B$ is true" | $P(4) \implies P(5)$ |
| $\sum_{i=1}^{n} i$ | "add up $i$ for $i$ from 1 to $n$" | $\sum_{i=1}^{3} i = 1+2+3$ |
:::

## 1. The idea in one picture

A professor lines up the class and makes two rules. The first student gets a candy bar. And if a student gets one, the next student does too.

<Predict question="You're student 17. Are you guaranteed a candy bar? What would have to go wrong for you not to get one?">

Yes. Student 0 gets one by rule 1. Rule 2 then passes it to student 1, then to 2, and so on: 17 uses of rule 2 reach you. The only ways you'd miss out are that **nobody starts** (rule 1 fails), or that **some student in front of you doesn't pass it on** (rule 2 fails for one student). The dominoes below let you try both.

</Predict>

<DominoChain />

That's all induction is. You never check infinitely many cases one by one. You check **two** things, and they hold up an infinite chain.

## 2. The rule, precisely

::: tip The Induction Principle
Let $P$ be a predicate on $\mathbb{N}$. If

1. $P(0)$ is true **(base case)**, and
2. for every $n \in \mathbb{N}$, $P(n) \implies P(n+1)$ **(inductive step)**,

then $P(m)$ is true for every $m \in \mathbb{N}$.
:::

Read the inductive step carefully. It does **not** say "$P(n)$ is true". It says "*if* $P(n)$ were true, then $P(n+1)$ would be true too". You get to **assume** $P(n)$ and then use it. That's what makes induction powerful: you build on a free assumption, and the base case backs it up.

<Checkpoint :n="1" :of="4" next="§3–4, the first real proof (about 15 min)" />

## 3. First proof: adding $1$ to $n$

$$1 + 2 + 3 + \cdots + n = \frac{n(n+1)}{2}$$

(This is equation 5.1 in the book.)

Before proving it, look at **why** it's true. A proof makes it certain; a picture shows you why.

<StaircaseSum />

Now the induction proof. Watch how the inductive step is exactly the "add one column" picture. Turn on *Highlight the step* above.

::: info Proof (the clean version, MCS p. 141)
We use induction. Let $P(n)$ be equation (5.1).

**Base case.** $P(0)$: the empty sum is $0$, and $\frac{0 \cdot 1}{2} = 0$. ✓

**Inductive step.** Assume $P(n)$ for some $n \ge 0$, that is, $1 + \cdots + n = \frac{n(n+1)}{2}$. Add $n+1$ to both sides:

$$\begin{aligned}
1 + \cdots + n + (n+1) &= \frac{n(n+1)}{2} + (n+1) \\
&= \frac{n(n+1) + 2(n+1)}{2} \\
&= \frac{(n+1)(n+2)}{2},
\end{aligned}$$

which is exactly $P(n+1)$. By induction, $P(n)$ holds for all $n \in \mathbb{N}$. $\blacksquare$
:::

Don't just read it. Explain it to yourself. For each line, ask *why does this follow?* (Explaining each line like this is the single best-supported habit for reading proofs. See [How these lessons teach](/guide/how-to-learn#self-explanation-especially-for-proofs).)

<Recall q="Why is it legal to 'add n+1 to both sides'? What exactly are we assuming at that moment?">

We're inside the inductive step, so we've assumed $P(n)$: the equation for $n$ holds. Adding the same quantity to both sides of a true equation gives a true equation. We never assumed $P(n+1)$. We *derived* it.

</Recall>

<Recall q="The base case is n = 0, an 'empty sum'. Why is starting at 0 fine, and what would change if we started at n = 1?">

The empty sum is $0$ by convention, and $\frac{0\cdot 1}{2}=0$, so $P(0)$ holds. Starting at $n=1$ also works ($1 = \frac{1\cdot2}{2}$). Then the conclusion covers $n \ge 1$. The base case just has to be the first domino you claim falls.

</Recall>

## 4. The template

Every induction proof has the same five parts. Use this as a checklist when you write your own.

1. **Say it's induction.** "We use induction on $n$."
2. **Write $P(n)$ down explicitly.** This is where most broken proofs go wrong. If you can't write it in one sentence, you aren't ready to prove it.
3. **Base case:** prove $P(0)$, or whatever the smallest $n$ is.
4. **Inductive step:** "Assume $P(n)$" … *(use it)* … "therefore $P(n+1)$." It must work for **every** $n$.
5. **Conclude:** "By induction, $P(n)$ holds for all $n$."

<Checkpoint :n="2" :of="4" next="§5–6, your proof and the courtyard puzzle (about 20 min)" />

## 5. Your turn: odd numbers

Claim: $1 + 3 + 5 + \cdots + (2n-1) = n^2$. Get a feel for it first:

<OddSquares />

Now fill in each blank yourself **before** you reveal it.

<Recall q="Step 2: what exactly is P(n)?">

$P(n)$: $\;\displaystyle\sum_{k=1}^{n} (2k-1) = n^2$.

</Recall>

<Recall q="Step 3: base case. Which n, and why is it true?">

$n = 0$: the empty sum is $0 = 0^2$. (Starting at $n=1$ also works: $1 = 1^2$.)

</Recall>

<Recall q="Step 4: assume P(n). What do you add to both sides, and what do you get?">

The next odd number is $2(n+1) - 1 = 2n + 1$. So
$$1 + 3 + \cdots + (2n-1) + (2n+1) = n^2 + 2n + 1 = (n+1)^2,$$
which is $P(n+1)$. In the picture, that's the next L-shaped layer turning an $n \times n$ square into an $(n+1) \times (n+1)$ one.

</Recall>

## 6. A harder one: Bill's courtyard

MIT plans a $2^n \times 2^n$ courtyard. One central square holds a statue of a donor, "Bill". Every other square must be covered by L-shaped tiles, each covering three squares.

<Predict question="Try the obvious induction: let P(n) be 'a 2ⁿ×2ⁿ courtyard with Bill in the centre can be tiled'. In the inductive step you split the big courtyard into four smaller ones. Why doesn't P(n) help you?">

When you split the big courtyard into four quadrants, Bill sits at a **corner** of one quadrant, not at its centre. The other three quadrants have no Bill at all. $P(n)$ only talks about Bill in the centre, so it says nothing useful about any of the four pieces. The step won't go through.

</Predict>

The book's trick is to **prove something stronger**:

> $P(n)$: for **every** location of Bill in a $2^n \times 2^n$ courtyard, the rest can be tiled.

This sounds harder, but it makes the inductive step easy. When you assume $P(n)$ you get to assume more, so you have more to work with. Split into four quadrants. Put one L tile on the centre squares of the three quadrants without Bill. Those three squares act as "temporary Bills". Now every quadrant is a $2^n \times 2^n$ courtyard with exactly one blocked square, which is exactly what $P(n)$ covers.

<TrominoTiling />

::: tip Strengthening the hypothesis
When an induction proof gets stuck, try proving a **stronger** statement. You have to prove more, but you also get to assume more. (The stronger claim still has to be true.)
:::

<Checkpoint :n="3" :of="4" next="§7–8 and the final check (about 10 min)" />

## 7. Where CS uses this

::: info Recursion is induction running backwards
```python
def total(n):          # claim: total(n) == n*(n+1)//2 for all n >= 0
    if n == 0:
        return 0       # base case
    return total(n - 1) + n   # assume total(n-1) is right, then add n
```
To prove this function is correct you write the proof from section 3, almost word for word. The base case is the `if`. The inductive step is "assume the recursive call returns the right answer". Every time you trust a recursive call while writing recursive code, you're relying on the inductive hypothesis.

The courtyard proof shows something else too: **the proof is a divide-and-conquer algorithm.** The visual above simply runs the proof. It splits into four, places one tile, and recurses. Merge sort and quadtrees have the same structure, and their correctness proofs have the same shape.
:::

## 8. Spot the bug

<Predict question="'Proof' that all horses are the same colour. P(n): in any set of n horses, all have the same colour. Base: one horse matches itself. Step: take n+1 horses. The first n are the same colour (by P(n)). The last n are the same colour. They overlap, so all n+1 match. Where does this break?">

The step fails at **$n = 1$**. With 2 horses, "the first 1" and "the last 1" are two different horses with **no overlap**, so nothing links them. The step holds for $n \ge 2$ but not for $n = 1$. That one broken link is the gap in the dominoes: go back up, untick the inductive step, and set the failure at $n = 1$. Everything after domino 1 stays standing.

</Predict>

## Check yourself

<Recall q="What are the two things every ordinary induction proof must establish?">

A base case $P(0)$, and an inductive step: $P(n) \implies P(n+1)$ for **every** $n \ge 0$.

</Recall>

<Recall q="In the inductive step, are you allowed to assume P(n)? Isn't that assuming what you're trying to prove?">

You assume $P(n)$ for **one** $n$ in order to prove $P(n+1)$. You're proving the *implication* $P(n) \implies P(n+1)$, not $P(n)$ itself. The base case starts the chain, and the implication carries it forward.

</Recall>

<Recall q="Why did the courtyard proof need 'Bill anywhere' rather than 'Bill in the centre'?">

After splitting, Bill (and the temporary Bills) sit at quadrant corners, not centres. Only the stronger hypothesis says anything about those smaller courtyards.

</Recall>

<Checkpoint :n="4" :of="4" />

---

**Next:** do the §5.1 problems at the end of chapter 5 in the textbook. Write each proof by hand using the five-part template, then ask the tutor to check it (see [Start here](/guide/start-here#the-ai-tutor)). Add the cards in `flashcards/05-1-induction.csv` to Anki.
