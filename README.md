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

| Folder | What's in it |
|---|---|
| `docs/lessons/` | One page per textbook section |
| `docs/components/` | Interactive visuals (Vue + SVG) |
| `flashcards/` | Anki decks, one per lesson |
| `progress/log.md` | Learning log, kept up to date by the tutor |
