# Start here

## What this is

A companion to [MIT 6.1200J, Spring 2024](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/) and its textbook, *Mathematics for Computer Science* (Lehman, Leighton, Meyer). Use it alongside the book and lectures, not instead of them. Each lesson covers one section of the book.

## A session, start to finish (about 60–90 minutes)

0. **Set a focus block.** Use the *Focus block* button at the bottom right of every lesson: one goal, one time box. Start with a length you can actually finish.
1. **Warm up (5 min).** Ask the tutor to *quiz me*. It pulls a few questions from earlier lessons.
2. **Watch, then read.** The [2024 lecture video](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/video_galleries/lecture-videos/), then that lecture's reading in `mcs.pdf` (see the [course map](./course-map)). Pause the video at each new definition and predict what comes next.
3. **Do the lesson (30 min).** Answer the Predict boxes *before* revealing them, and play with every visual.
4. **Practise (30+ min).** Do the textbook problems by hand. Stuck? Ask the tutor for *a hint*, not the answer.
5. **Close (5 min).** Ask the tutor to *log this session*. Import the lesson's flashcards into Anki.

## Rusty after a long break?

Don't do a big refresher up front. Each lesson opens a **Notation refresher** box right where a symbol first appears, so you only review what you actually need, when you need it. If algebra itself feels shaky (expanding $(n+1)(n+2)$, working with fractions, using exponent rules), ask the tutor to *check my prerequisites*. It gives you a 10-question diagnostic and drills only what you miss.

## The AI tutor

Open this repo in [Claude Code](https://claude.com/claude-code). It reads `CLAUDE.md` and becomes a tutor for this course. Things to say to it:

| You say | It does |
|---|---|
| *teach me 5.2* | Runs a guided session: you try first, then a worked example, then a faded one |
| *hint* | Gives the smallest useful nudge. Ask again for a bigger one |
| *check my proof* (paste or point at a file) | Has you explain your key lines first, then gives feedback against the five-part template. It points to where the problem is but doesn't rewrite it for you |
| *quiz me* | Mixed, spaced recall questions from what you've covered so far |
| *teach-back induction* | Plays a confused student. You explain, and it asks the questions a real student would |
| *break a proof* | Writes a subtly wrong proof for you to debug |
| *read 5.2* | Assigns exact pages of `mcs.pdf` with focus questions, then quizzes you on them |
| *show me why …* | Builds a custom interactive visual for exactly what's confusing you |
| *lab 5.1* | Conjecture lab: compute examples in Python, guess the pattern, then prove it |
| *review my proof PR 3* | Reviews a proof you pushed under `proofs/` line by line, like code review |
| *mock exam induction* | A timed, closed-book exam. No help until you submit, then graded |
| *log this session* | Updates `progress/log.md`: what you covered, what was shaky, when to review |

Why it works this way is on [How these lessons teach](./how-to-learn#using-ai-without-letting-it-do-the-learning).

## Run the site locally

```sh
npm install
npm run dev     # http://localhost:5173/math/
```
