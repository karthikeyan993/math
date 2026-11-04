"""Cross-check the interactive components' maths against independent Python.

1. Every <TruthTable vars=... cols=...> in docs/lessons/*.md: the TypeScript
   evaluator (docs/components/logic.ts, run under Node) and the Python copy
   (tools/verify/_logic.py) must produce the same table, and both must agree
   with the textbook's own truth tables (MCS §3.1, pp. 48–50).
2. Grammar edge cases: both parsers must accept and reject the same formulas.
3. Every QuantifierGame statement (docs/components/quantifiers.ts): its
   computed truth value must match a Python evaluation.
"""

import html
import json
import re
import subprocess
from pathlib import Path

from _common import check, done
import _logic

ROOT = Path(__file__).resolve().parents[2]
LOGIC_TS = (ROOT / "docs/components/logic.ts").as_uri()
QUANT_TS = (ROOT / "docs/components/quantifiers.ts").as_uri()


def node(js: str):
    out = subprocess.run(["node", "--input-type=module", "-e", js], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


# --- 1. Truth tables used in lessons --------------------------------------
tables = []
for md in sorted((ROOT / "docs/lessons").glob("*.md")):
    for tag in re.findall(r"<TruthTable\b[^>]*>", md.read_text(), flags=re.S):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', tag))
        tables.append({"where": md.name, "vars": [v.strip() for v in attrs["vars"].split(",")],
                       "cols": [html.unescape(c).strip() for c in attrs["cols"].split(";")]})

ts_tables = node(
    f"import {{ table }} from '{LOGIC_TS}';"
    f"const t = {json.dumps(tables)};"
    "console.log(JSON.stringify(t.map(x => table(x.vars, x.cols))));"
) if tables else []
for t, ts in zip(tables, ts_tables):
    check(f"{t['where']}: TS and Python agree on {t['cols']}", ts == _logic.table(t["vars"], t["cols"]))

# The textbook's tables, copied by hand from MCS pp. 48–50 (rows TT, TF, FT, FF).
BOOK = {"P AND Q": "TFFF", "P OR Q": "TTTF", "P XOR Q": "FTTF", "P IFF Q": "TFFT", "P IMPLIES Q": "TFTT"}
ts_book = node(f"import {{ table }} from '{LOGIC_TS}'; console.log(JSON.stringify(table(['P','Q'], {json.dumps(list(BOOK))})))")
check("TS matches the book's AND/OR/XOR/IFF/IMPLIES tables", ts_book == list(BOOK.values()))
check("Python matches the book's AND/OR/XOR/IFF/IMPLIES tables", _logic.table(["P", "Q"], list(BOOK)) == list(BOOK.values()))
check("NOT matches the book (p. 48)", _logic.table(["P"], ["NOT P"]) == ["FT"])

# --- 2. Grammar edge cases: same accept/reject decisions --------------------
CASES = ["NOT A AND B", "NOT(A AND B)", "A AND B OR C", "A IMPLIES B IMPLIES C", "A IFF B IFF C",
         "(A IMPLIES B) IMPLIES C", "A OR B OR C", "A XOR B XOR C", "A AND", "(A", "A)", "A + B", "NOT NOT A"]

def py_result(src):
    try:
        return _logic.table(sorted(set(re.findall(r"\b[A-C]\b", src))), [src])[0]
    except (ValueError, KeyError):
        return "ERROR"

ts_cases = node(
    f"import {{ table }} from '{LOGIC_TS}';"
    f"const cs = {json.dumps(CASES)};"
    "console.log(JSON.stringify(cs.map(c => { try { const vs = [...new Set(c.match(/\\b[A-C]\\b/g) ?? [])].sort();"
    " return table(vs, [c])[0] } catch (e) { return 'ERROR' } })));"
)
for src, ts in zip(CASES, ts_cases):
    check(f"grammar agrees on {src!r} (TS {ts}, Python {py_result(src)})", ts == py_result(src))
check("NOT binds to one atom: NOT A AND B = (NOT A) AND B", py_result("NOT A AND B") == "FFTF")
check("mixing AND/OR without parentheses is rejected", py_result("A AND B OR C") == "ERROR")

# --- 3. Quantifier game statements ----------------------------------------
D = range(5)
PY_STATEMENTS = {
    "sum-AE": all(any(x + y == 4 for y in D) for x in D),
    "sum-EA": any(all(x + y == 4 for x in D) for y in D),
    "bigger-AE": all(any(y > x for y in D) for x in D),
    "max-EA": any(all(y >= x for x in D) for y in D),
}
ts_stmts = node(
    f"import {{ STATEMENTS, DOMAIN, truth }} from '{QUANT_TS}';"
    "console.log(JSON.stringify({domain: DOMAIN, s: STATEMENTS.map(s => [s.id, truth(s)])}));"
)
check("game domain is {0, 1, 2, 3, 4}", ts_stmts["domain"] == list(D))
check("every game statement has a Python twin", sorted(i for i, _ in ts_stmts["s"]) == sorted(PY_STATEMENTS))
for sid, val in ts_stmts["s"]:
    check(f"game statement {sid}: TS says {val}, Python says {PY_STATEMENTS.get(sid)}", val == PY_STATEMENTS.get(sid))
check("expected truth values: T, F, F, T", [PY_STATEMENTS[k] for k in ["sum-AE", "sum-EA", "bigger-AE", "max-EA"]] == [True, False, False, True])

# --- 4. numbers.ts (PrimeStreak, FactorSigns) ------------------------------
from _common import is_prime
NUMBERS_TS = (ROOT / "docs/components/numbers.ts").as_uri()
ts_num = node(
    f"import {{ isPrime, factor, euler, cubic }} from '{NUMBERS_TS}';"
    "const ns = [...Array(200).keys()];"
    "console.log(JSON.stringify({ prime: ns.map(isPrime), euler: ns.map(euler),"
    " factor: ns.slice(2).map(factor), cubic: [-3, -2, -1, 0, 0.5, 1, 2, 3].map(cubic) }));"
)
check("numbers.ts isPrime agrees with Python for 0..199", ts_num["prime"] == [is_prime(n) for n in range(200)])
check("numbers.ts euler(n) = n^2 + n + 41", ts_num["euler"] == [n * n + n + 41 for n in range(200)])
def py_factor(n):
    out, d = [], 2
    while d * d <= n:
        while n % d == 0:
            out.append(d); n //= d
        d += 1
    return out + ([n] if n > 1 else [])
check("numbers.ts factor agrees with Python for 2..199", ts_num["factor"] == [py_factor(n) for n in range(2, 200)])
check("numbers.ts cubic(x) = -x^3 + 4x + 1", ts_num["cubic"] == [-x**3 + 4 * x + 1 for x in [-3, -2, -1, 0, 0.5, 1, 2, 3]])

# --- 5. party.ts (PartyGraph) vs Python, on random colourings ----------------
import itertools, random
rng = random.Random(1200)
PARTY_TS = (ROOT / "docs/components/party.ts").as_uri()
configs = []
for _ in range(300):
    n = rng.choice([3, 4, 5, 6])
    configs.append({"n": n, "edges": {f"{i}-{j}": rng.choice(["met", "not", None])
                                      for i, j in itertools.combinations(range(n), 2)}})
ts_tri = node(
    f"import {{ monoTriangles }} from '{PARTY_TS}';"
    f"const cs = {json.dumps(configs)};"
    "console.log(JSON.stringify(cs.map(c => { const e = {}; for (const k in c.edges) if (c.edges[k]) e[k] = c.edges[k];"
    " return monoTriangles(c.n, e).map(t => [t.people, t.kind]) })));"
)
def py_tri(c):
    e = c["edges"]
    return [[[a, b, d], e[f"{a}-{b}"]] for a, b, d in itertools.combinations(range(c["n"]), 3)
            if e[f"{a}-{b}"] and e[f"{a}-{b}"] == e[f"{a}-{d}"] == e[f"{b}-{d}"]]
check("party.ts finds exactly the same one-colour triangles as Python (300 random graphs)",
      ts_tri == [py_tri(c) for c in configs])

# --- 6. gridStatements (QuantifierGrid) vs Python, on random grids -----------
grids = [[[rng.random() < p for _ in range(5)] for _ in range(5)] for p in (0.1, 0.3, 0.5, 0.8) for _ in range(50)]
ts_grid = node(
    f"import {{ gridStatements }} from '{QUANT_TS}';"
    f"console.log(JSON.stringify({json.dumps(grids)}.map(gridStatements)));"
)
def py_grid(P):
    R = range(5)
    return {"AxEy": all(any(P[x][y] for y in R) for x in R), "EyAx": any(all(P[x][y] for x in R) for y in R),
            "ExAy": any(all(P[x][y] for y in R) for x in R), "AyEx": all(any(P[x][y] for x in R) for y in R)}
check("gridStatements agrees with Python on 200 random grids", ts_grid == [py_grid(g) for g in grids])

# --- 7. Every WasonCards answer in the lessons, re-derived ------------------
# Supports the vowel/even rule: letters are vowels or not, numbers even or not.
for md in sorted((ROOT / "docs/lessons").glob("*.md")):
    for tag in re.findall(r"<WasonCards\b[^>]*>", md.read_text(), flags=re.S):
        a = dict(re.findall(r'(\w+)="([^"]*)"', tag))
        check(f"{md.name}: WasonCards rule is the supported vowel/even rule",
              a["rule"] == "If a card has a vowel on one side, then it has an even number on the other side.")
        faces = [f.strip() for f in a["cards"].split(",")]
        def must_turn(face):
            if face.isalpha():  # hidden side is a number; breaks if vowel and odd
                return face.upper() in "AEIOU"
            return int(face) % 2 == 1  # hidden side is a letter; breaks if odd and vowel
        derived = [i for i, f in enumerate(faces) if must_turn(f)]
        check(f"{md.name}: WasonCards answer {a['answer']} matches brute force {derived}",
              [int(i) for i in a["answer"].split(",")] == derived)

# --- 8. Every EquivalenceChecker in the lessons parses in both evaluators ----
for md in sorted((ROOT / "docs/lessons").glob("*.md")):
    for tag in re.findall(r"<EquivalenceChecker\b[^>]*>", md.read_text(), flags=re.S):
        a = dict(re.findall(r'(\w+)="([^"]*)"', tag))
        l, r = html.unescape(a["left"]), html.unescape(a["right"])
        vs = sorted(set(re.findall(r"\b(?!NOT\b|AND\b|OR\b|XOR\b|IMPLIES\b|IFF\b)[A-Za-z_]\w*", l + " " + r)))
        ts = node(f"import {{ table }} from '{LOGIC_TS}'; console.log(JSON.stringify(table({json.dumps(vs)}, {json.dumps([l, r])})))")
        check(f"{md.name}: EquivalenceChecker {l!r} vs {r!r}: TS and Python agree", ts == _logic.table(vs, [l, r]))

done()
