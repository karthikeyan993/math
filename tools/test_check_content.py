#!/usr/bin/env python3
"""Test the checker itself: plant one known mistake at a time, expect a failure.

    python3 tools/test_check_content.py

Works on a temporary copy of the repo, so nothing here touches your files.
A checker that never fails proves nothing; this shows each check can fail.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (file, old text, new text, expected substring in the checker's output, needs full run)
MUTATIONS = [
    ("docs/lessons/01-proofs.md", "either true or false.", "either true or untrue.", "quote not found", False),
    ("docs/lessons/01-proofs.md", "(MCS §1.2, p. 8). With", "(MCS §1.2, p. 18). With", "§1.2 runs", False),
    ("docs/lessons/01-proofs.md", "**Problem 1.7** (p. 24", "**Problem 1.7** (p. 25", "Problem 1.7 is not on printed page 25", False),
    ("docs/lessons/01-proofs.md", "**Theorem 1.5.1** (MCS p. 12)", "**Theorem 1.5.1** (MCS p. 13)", "Theorem 1.5.1 is not on printed page 13", False),
    ("docs/lessons/03-6-quantifiers.md", "(MCS §3.6.6, p. 67)", "(MCS §3.9, p. 67)", "§3.9 is not a section", False),
    ("docs/lessons/03-6-quantifiers.md", "**Problem 3.27** (p. 87", "**Problem 3.99** (p. 87", "Problem 3.99", False),
    ("docs/lessons/01-proofs.md", "<PrimeStreak />", "<PrimeStreek />", "<PrimeStreek> is not registered", False),
    ("docs/lessons/05-1-induction.md", "/guide/start-here#the-ai-tutor", "/guide/start-here#no-such-heading", "no heading with that anchor", False),
    ("docs/lessons/01-proofs.md", "the number $p(n) = n^2 + n + 41$ is prime", "the number $p(n) = n^2 + n + 41 is prime", "odd number of $ signs", False),
    ("flashcards/01-proofs.csv", 'a <code>bool</code>.","mcs::ch01"', 'a <code>bool</code>."', "card 1 needs exactly 3", False),
    ("docs/lessons/03-1-propositional-logic.md", "(MCS §3.1.1, p. 49)", "(MCS §3.1.9, p. 49)", "§3.1.9 is not a section", False),
    ("docs/lessons/03-1-propositional-logic.md", "<cite>MCS §3.1.3, p. 50</cite>", "<cite>MCS §3.1.3, p. 49</cite>", "§3.1.3 runs", False),
    ("flashcards/03-6-quantifiers.csv", "(MCS §3.6.5, p. 66)", "(MCS §3.6.5, p. 61)", "§3.6.5 runs", False),
    ("docs/.vitepress/config.mts", "link: '/lessons/03-6-quantifiers'", "link: '/lessons/03-6-quantifier'", "doesn't resolve", False),
    ("docs/lessons/03-1-propositional-logic.md", 'cards="A, K, 4, 7" answer="0,3"', 'cards="A, K, 4, 7" answer="0,2"', "WasonCards answer", True),
    ("docs/components/logic.ts", "case 'IMPLIES': return !v[0] || v[1]", "case 'IMPLIES': return v[0] || v[1]", "TS and Python agree", True),
    ("docs/components/quantifiers.ts", "pred: ({ x, y }) => y > x,", "pred: ({ x, y }) => y >= x,", "game statement bigger-AE", True),
    ("tools/verify/01-proofs.py", "p(40) == 1681 == 41 * 41", "p(40) == 1681 == 41 * 43", "FAILED", True),
]


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        ignore = shutil.ignore_patterns("node_modules", "dist", "cache", "__pycache__")
        for d in ("docs", "tools", "flashcards", "lab"):
            shutil.copytree(ROOT / d, t / d, ignore=ignore)
        (t / "mcs.pdf").symlink_to(ROOT / "mcs.pdf")

        def run(full: bool) -> subprocess.CompletedProcess:
            args = [sys.executable, str(t / "tools/check_content.py")] + ([] if full else ["--quick"])
            return subprocess.run(args, capture_output=True, text=True, cwd=t)

        base = run(full=True)
        if base.returncode != 0:
            print("The unmodified repo doesn't pass the checker; fix that first:\n" + base.stdout)
            return 1

        bad = 0
        for path, old, new, expect, full in MUTATIONS:
            f = t / path
            original = f.read_text()
            if original.count(old) != 1:
                print(f"✗ mutation target not found exactly once in {path}: {old!r}")
                bad += 1
                continue
            f.write_text(original.replace(old, new))
            r = run(full)
            f.write_text(original)
            out = r.stdout + r.stderr
            if r.returncode == 1 and expect in out:
                print(f"✓ caught: {path}: {old!r} → {new!r}")
            else:
                print(f"✗ NOT caught: {path}: {old!r} → {new!r} (expected {expect!r})\n{out[-600:]}")
                bad += 1
        print(f"\n{len(MUTATIONS) - bad} of {len(MUTATIONS)} planted mistakes caught.")
        return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
