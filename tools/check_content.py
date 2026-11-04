#!/usr/bin/env python3
"""Check the lessons for the mistakes an AI (or a tired human) is likely to make.

    python3 tools/check_content.py          # everything
    python3 tools/check_content.py --quick  # skip running the verify and lab scripts

What it checks, for every lesson in docs/lessons/:

1. Citations. Every "§X.Y, p. N" / "§X.Y (pp. A–B)" names a real section,
   and the pages fall inside that section (tools/mcs-index.tsv).
2. Quotes. Every blockquote ending in <cite>MCS §X, p. N</cite> appears
   word for word on printed page N (or N + 1) of mcs.pdf.
3. Labels. Every "Problem X.Y (p. N)" or "Theorem X.Y.Z (MCS p. N)"
   exists on that page of mcs.pdf; every other "Problem X.Y" exists somewhere.
4. Components. Every <Component> used is registered in the theme and exists.
5. Links. Every internal link (and #anchor) resolves; every lesson is in the
   sidebar and the course map.
6. Flashcards. flashcards/<lesson>.csv exists and every row has 3 fields.
7. Maths. tools/verify/<lesson>.py exists, and every script in tools/verify/
   and lab/ runs without error. Those scripts brute-force each numeric or
   finite claim the lesson makes.
8. Inline maths. Every line has an even number of $ signs.

Exit status 1 if anything fails. Needs pdftotext (poppler-utils) and node.
"""

from __future__ import annotations

import csv
import io
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LESSONS = sorted((DOCS / "lessons").glob("*.md"))
errors: list[str] = []


def fail(where: str, msg: str) -> None:
    errors.append(f"{where}: {msg}")


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


# ---------------------------------------------------------------- index + pdf
INDEX = []  # (section, printed_page, pdf_page, title) in book order
for line in (ROOT / "tools/mcs-index.tsv").read_text().splitlines()[1:]:
    sec, printed, pdf, title = line.split("\t")
    if not INDEX or INDEX[-1][0] != sec:
        INDEX.append((sec, int(printed), int(pdf), title))
SECTIONS = {s: i for i, (s, *_rest) in enumerate(INDEX)}
MAX_PAGE = max(r[1] for r in INDEX)


def _indexed_range(key: str) -> tuple[int, int]:
    i = SECTIONS[key]
    start, end = INDEX[i][1], MAX_PAGE
    for s, printed, *_ in INDEX[i + 1:]:
        if not (s == key or s.startswith(key + ".")):
            end = printed
            break
    return start, end


def section_range(sec: str) -> tuple[int, int] | None:
    """Printed page range of a chapter or section (from the index).

    Subsections like 1.4.1 aren't in the index: they must appear as a heading
    line in mcs.pdf inside their parent section, and their range starts there.
    """
    if sec in SECTIONS:
        return _indexed_range(sec)
    parts = sec.split(".")
    parent = ".".join(parts[:2])
    if len(parts) < 3 or parent not in SECTIONS:
        return None
    start, end = _indexed_range(parent)
    heading = re.compile(rf"^\s*{re.escape(sec)}\s*$", re.M)
    for page in range(start, end + 1):
        if heading.search(pdf_text(page)):
            return page, end
    return None


def pdf_page_of(printed: int) -> int:
    """Map a printed page to a PDF page using the nearest index row at or before it."""
    best = min(INDEX, key=lambda r: (printed - r[1] if printed >= r[1] else 10**9))
    return printed + (best[2] - best[1])


_pdf_pages: list[str] | None = None


def pdf_text(printed: int) -> str:
    global _pdf_pages
    if _pdf_pages is None:
        out = subprocess.run(["pdftotext", "-enc", "UTF-8", str(ROOT / "mcs.pdf"), "-"],
                             capture_output=True, text=True, check=True).stdout
        _pdf_pages = out.split("\f")
    i = pdf_page_of(printed) - 1
    return _pdf_pages[i] if 0 <= i < len(_pdf_pages) else ""


def norm(s: str) -> str:
    """Letters and digits only: robust to line breaks, hyphenation, quotes, ligatures."""
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"[^a-z0-9]", "", s)


def strip_code(md: str) -> str:
    """Blank out fenced code blocks, keeping line numbers."""
    return re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), md, flags=re.S)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


# ------------------------------------------------------------------ checks 1–3
CITE = re.compile(r"§(\d+(?:\.\d+)*)(?:\s*[–-]\s*(\d+(?:\.\d+)*))?(?:[^§\n]{0,6}?\bpp?\.\s*(\d+)(?:\s*[–-]\s*(\d+))?)?")
LABEL = re.compile(r"\b(Problem|Theorem|Proposition|Claim|Corollary|Lemma)\s+(\d+\.\d+(?:\.\d+)?)\**\s*\((?:MCS\s+)?pp?\.\s*(\d+)")
ANY_PROBLEM = re.compile(r"\bProblem\s+(\d+\.\d+)\b")
QUOTE = re.compile(r"((?:^>.*\n?)+)", re.M)
CITE_TAG = re.compile(r"<cite>MCS\s+(?:§[\d.]+,\s*)?p\.\s*(\d+)</cite>")

_problem_pages: dict[str, list[int]] | None = None


def problem_pages() -> dict[str, list[int]]:
    global _problem_pages
    if _problem_pages is None:
        pdf_text(1)
        _problem_pages = {}
        for i, page in enumerate(_pdf_pages or []):
            for num in re.findall(r"^Problem (\d+\.\d+)\.", page, flags=re.M):
                _problem_pages.setdefault(num, []).append(i + 1)
    return _problem_pages


def check_citations(path: Path, text: str) -> None:
    body = strip_code(text)
    for m in CITE.finditer(body):
        a, b, p1, p2 = m.groups()
        where = f"{rel(path)}:{line_of(body, m.start())}"
        ra, rb = section_range(a), section_range(b or a)
        if ra is None or rb is None:
            fail(where, f"§{a}{'–' + b if b else ''} is not a section in tools/mcs-index.tsv")
            continue
        if p1:
            lo, hi = int(p1), int(p2 or p1)
            if not (ra[0] <= lo <= hi <= rb[1]):
                fail(where, f"§{a}{'–' + b if b else ''} runs pp. {ra[0]}–{rb[1]}, but the citation says pp. {lo}–{hi}")
    for m in LABEL.finditer(body):
        kind, num, page = m.group(1), m.group(2), int(m.group(3))
        where = f"{rel(path)}:{line_of(body, m.start())}"
        if norm(f"{kind} {num}") not in norm(pdf_text(page)):
            fail(where, f"{kind} {num} is not on printed page {page} of mcs.pdf")
    for m in ANY_PROBLEM.finditer(body):
        if m.group(1) not in problem_pages():
            fail(f"{rel(path)}:{line_of(body, m.start())}", f"Problem {m.group(1)} doesn't exist in mcs.pdf")


def check_quotes(path: Path, text: str) -> None:
    for m in QUOTE.finditer(text):
        block = m.group(1)
        cite = CITE_TAG.search(block)
        if not cite:
            continue
        page = int(cite.group(1))
        quote = CITE_TAG.sub("", re.sub(r"^>\s?", "", block, flags=re.M))
        quote = re.sub(r"[*_`]", "", quote)
        haystack = norm(pdf_text(page) + pdf_text(page + 1))
        if norm(quote) not in haystack:
            fail(f"{rel(path)}:{line_of(text, m.start())}",
                 f"quote not found on printed page {page}: {quote.strip()[:70]!r}")


# -------------------------------------------------------------------- check 4
THEME = (DOCS / ".vitepress/theme/index.ts").read_text()
REGISTERED = set(re.findall(r"app\.component\('(\w+)'", THEME))
HTML_TAGS = {"div", "span", "cite", "b", "i", "br", "details", "summary", "p", "a", "code", "table"}


def check_components(path: Path, text: str) -> None:
    for m in re.finditer(r"<([A-Z]\w*)\b", strip_code(text)):
        name = m.group(1)
        where = f"{rel(path)}:{line_of(text, m.start())}"
        if name not in REGISTERED:
            fail(where, f"<{name}> is not registered in docs/.vitepress/theme/index.ts")
        if not (DOCS / "components" / f"{name}.vue").exists():
            fail(where, f"docs/components/{name}.vue does not exist")


# -------------------------------------------------------------------- check 5
def slug(heading: str) -> str:
    h = re.sub(r"<[^>]+>", "", heading)
    h = re.sub(r"[$`*_]", "", h).lower()
    h = re.sub(r"[^\w\- ]", "", h).strip()
    return re.sub(r"-{2,}", "-", re.sub(r"\s+", "-", h))


def anchors(md: Path) -> set[str]:
    return {slug(h) for h in re.findall(r"^#{1,6}\s+(.*)$", strip_code(md.read_text()), flags=re.M)}


def resolve(link: str) -> Path | None:
    path = link.split("#")[0].rstrip("/")
    for cand in (DOCS / f"{path.lstrip('/')}.md", DOCS / path.lstrip("/") / "index.md"):
        if cand.exists():
            return cand
    return None


def check_links() -> None:
    pages = [p for p in DOCS.rglob("*.md") if "node_modules" not in p.parts and ".vitepress" not in p.parts]
    for md in pages:
        text = strip_code(md.read_text())
        for m in re.finditer(r"\]\((/[^)\s]*)\)", text):
            link = m.group(1)
            target = resolve(link)
            where = f"{rel(md)}:{line_of(text, m.start())}"
            if target is None:
                fail(where, f"link {link} doesn't resolve to a page")
            elif "#" in link and link.split("#", 1)[1] not in anchors(target):
                fail(where, f"link {link}: no heading with that anchor in {rel(target)}")
    config = (DOCS / ".vitepress/config.mts").read_text()
    for link in re.findall(r"link:\s*'(/[^']*)'", config):
        if resolve(link) is None:
            fail("docs/.vitepress/config.mts", f"sidebar/nav link {link} doesn't resolve")
    course_map = (DOCS / "guide/course-map.md").read_text()
    for lesson in LESSONS:
        url = f"/lessons/{lesson.stem}"
        if f"'{url}'" not in config:
            fail(rel(lesson), f"not in the sidebar (docs/.vitepress/config.mts)")
        if f"({url})" not in course_map:
            fail(rel(lesson), f"not linked from docs/guide/course-map.md")


# -------------------------------------------------------------------- check 6
def check_flashcards(lesson: Path) -> None:
    f = ROOT / "flashcards" / f"{lesson.stem}.csv"
    if not f.exists():
        fail(rel(lesson), f"missing flashcards/{lesson.stem}.csv")
        return
    lines = f.read_text().splitlines()
    header = [l for l in lines if l.startswith("#")]
    for required in ("#separator:comma", "#html:true", "#tags column:3"):
        if required not in header:
            fail(rel(f), f"missing Anki header line {required}")
    rows = list(csv.reader(io.StringIO("\n".join(l for l in lines if l and not l.startswith("#")))))
    if not rows:
        fail(rel(f), "no cards")
    for i, row in enumerate(rows, 1):
        if len(row) != 3 or not all(c.strip() for c in row):
            fail(rel(f), f"card {i} needs exactly 3 non-empty fields (front, back, tags), got {len(row)}")
        elif not row[2].startswith("mcs::"):
            fail(rel(f), f"card {i} tags should start with mcs::")


# -------------------------------------------------------------------- check 7
def run_scripts() -> None:
    scripts = sorted(p for p in (ROOT / "tools/verify").glob("*.py") if not p.name.startswith("_"))
    scripts += sorted((ROOT / "lab").glob("*.py"))
    for s in scripts:
        try:
            r = subprocess.run([sys.executable, str(s)], cwd=ROOT, capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            fail(rel(s), "timed out")
            continue
        if r.returncode != 0:
            tail = (r.stdout + r.stderr).strip().splitlines()[-8:]
            fail(rel(s), "failed:\n    " + "\n    ".join(tail))
        elif "verify" in s.parts:
            print("  " + r.stdout.strip().splitlines()[-1])


# -------------------------------------------------------------------- check 8
def check_dollars(path: Path, text: str) -> None:
    for i, line in enumerate(strip_code(text).splitlines(), 1):
        if line.strip().startswith("$$"):
            continue
        if len(re.findall(r"(?<!\\)\$", line.replace("$$", ""))) % 2:
            fail(f"{rel(path)}:{i}", "odd number of $ signs (unclosed inline maths?)")


def main() -> int:
    quick = "--quick" in sys.argv
    for lesson in LESSONS:
        text = lesson.read_text()
        check_citations(lesson, text)
        check_quotes(lesson, text)
        check_components(lesson, text)
        check_flashcards(lesson)
        check_dollars(lesson, text)
        if not (ROOT / "tools/verify" / f"{lesson.stem}.py").exists():
            fail(rel(lesson), f"missing tools/verify/{lesson.stem}.py (brute-force checks of its claims)")
    for cards in sorted((ROOT / "flashcards").glob("*.csv")):
        check_citations(cards, cards.read_text())
    check_links()
    if not quick:
        print("Running verify and lab scripts:")
        run_scripts()
    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors:
            print("  ✗ " + e)
        return 1
    print(f"\nAll checks passed for {len(LESSONS)} lessons.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
