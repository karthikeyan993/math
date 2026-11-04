# Math for CS, visually

A self-study companion to [MIT 6.1200J Mathematics for Computer Science (Spring 2024)](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/): interactive lessons, real CS connections, and an AI tutor set up to help you learn rather than do the work for you.

- **Site:** https://karthikeyan993.github.io/math/ (deployed from `main` by GitHub Actions)
- **Start here:** [`docs/guide/start-here.md`](docs/guide/start-here.md)
- **Why it's built this way:** [`docs/guide/how-to-learn.md`](docs/guide/how-to-learn.md)
- **Tutor:** open the repo in Claude Code. [`CLAUDE.md`](CLAUDE.md) sets it up as a course tutor.

```sh
npm install
npm run dev
```

Before pushing lesson changes:

```sh
python3 tools/check_content.py   # citations, quotes, maths claims, links, flashcards
npm run build
node tools/smoke_test.cjs        # drives every visual in Chromium
```

| Folder | What's in it |
|---|---|
| `docs/lessons/` | One page per textbook section |
| `docs/components/` | Interactive visuals (Vue + SVG) |
| `flashcards/` | Anki decks, one per lesson |
| `lab/` | Python conjecture-lab worksheets |
| `tools/verify/` | Brute-force checks of every numeric or finite claim in each lesson |
| `tools/check_content.py` | Checks citations, quotes (against `mcs.pdf`), links, components and flashcards, and runs every verify script |
| `progress/log.md` | Learning log, kept up to date by the tutor |
| `mcs.pdf` | The textbook: *Mathematics for Computer Science*, Lehman, Leighton & Meyer (2018). [CC BY-SA](https://creativecommons.org/licenses/by-sa/3.0/), via [MIT OCW](https://ocw.mit.edu/courses/6-1200j-mathematics-for-computer-science-spring-2024/pages/readings/) |
