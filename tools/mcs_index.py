r"""Build tools/mcs-index.tsv: section -> printed page -> PDF page, from the mcs.pdf table of contents.

Run once (needs `pdftotext` from poppler-utils):  python3 tools/mcs_index.py
Then look sections up without opening the PDF:    grep -P '^3\.6\t' tools/mcs-index.tsv
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "mcs.pdf"
OUT = ROOT / "tools" / "mcs-index.tsv"


def pdf_text(first, last):
    return subprocess.run(
        ["pdftotext", "-layout", "-f", str(first), "-l", str(last), str(PDF), "-"],
        capture_output=True, text=True, check=True,
    ).stdout


def page_offset():
    """PDF page minus printed page, read from the running header ('page 105 — #113')."""
    m = re.search(r"page (\d+) — #(\d+)", pdf_text(113, 113))
    return int(m.group(2)) - int(m.group(1))


def main():
    offset = page_offset()
    entry = re.compile(r"^\s+(\d+(?:\.\d+)*)\s+(\S.*?)\s+(\d+)\s*$")
    rows, seen = [], set()
    for line in pdf_text(3, 30).splitlines():
        m = entry.match(line)
        if not m:
            continue
        sec, title, printed = m.group(1), re.sub(r"\s+", " ", m.group(2)), int(m.group(3))
        if sec in seen:
            continue
        seen.add(sec)
        rows.append(f"{sec}\t{printed}\t{printed + offset}\t{title}")
    OUT.write_text("section\tprinted_page\tpdf_page\ttitle\n" + "\n".join(rows) + "\n")
    print(f"wrote {len(rows)} entries to {OUT.relative_to(ROOT)} (pdf_page = printed_page + {offset})")


if __name__ == "__main__":
    main()
