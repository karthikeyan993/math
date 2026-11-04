"""Conjecture lab for MCS 5.1 (ordinary induction).

Work top to bottom. Each part: compute, look, guess, test. Then go prove it.
"""

# --- Part 1: sum of the first n numbers ------------------------------------
# Compute, then stare at the table. Before scrolling down, guess a formula.
print("n  1+..+n  n*(n+1)")
for n in range(1, 11):
    print(f"{n:<2} {sum(range(1, n + 1)):<7} {n * (n + 1)}")

# TODO: write your guess as a Python function, then run the check below.
def guess_sum(n: int) -> int | None:
    return None  # TODO: replace with your formula


if guess_sum(1) is None:
    print("Part 1: write guess_sum, then rerun.\n")
else:
    bad = next((n for n in range(10_000) if guess_sum(n) != sum(range(1, n + 1))), None)
    print("Part 1: guess holds for every n < 10,000. Evidence, not proof.\n" if bad is None else f"Part 1: guess fails at n = {bad}\n")


# --- Part 2: sum of the first n odd numbers --------------------------------
print("n  1+3+..+(2n-1)")
for n in range(1, 11):
    print(f"{n:<2} {sum(2 * k - 1 for k in range(1, n + 1))}")
# TODO: what's the pattern? Write guess_odd(n) and test it like Part 1.


# --- Part 3: the courtyard -------------------------------------------------
# The induction proof in MCS 5.1.5 is an algorithm. Here it is in code.
# Check that it really works for EVERY position of Bill, for small n.
def tile(n: int, bill: tuple[int, int]) -> dict[tuple[int, int], int]:
    """Return {cell: tile_id} covering every cell of a 2^n x 2^n board except bill."""
    board: dict[tuple[int, int], int] = {}
    next_id = 0

    def solve(x: int, y: int, size: int, b: tuple[int, int]) -> None:
        nonlocal next_id
        if size == 1:
            return  # base case: Bill fills the 1x1 courtyard
        h = size // 2
        quads = [(x, y), (x + h, y), (x, y + h), (x + h, y + h)]
        centres = [(x + h - 1, y + h - 1), (x + h, y + h - 1), (x + h - 1, y + h), (x + h, y + h)]
        inside = [qx <= b[0] < qx + h and qy <= b[1] < qy + h for qx, qy in quads]
        for i, c in enumerate(centres):
            if not inside[i]:
                board[c] = next_id  # three temporary Bills = one L tile
        next_id += 1
        for i, (qx, qy) in enumerate(quads):
            solve(qx, qy, h, b if inside[i] else centres[i])

    solve(0, 0, 2**n, bill)
    return board


def is_valid_tiling(n: int, bill: tuple[int, int], board: dict[tuple[int, int], int]) -> bool:
    size = 2**n
    every_cell = {(c, r) for c in range(size) for r in range(size)}
    if set(board) != every_cell - {bill}:
        return False
    tiles: dict[int, list[tuple[int, int]]] = {}
    for cell, t in board.items():
        tiles.setdefault(t, []).append(cell)
    for cells in tiles.values():
        xs = {c for c, _ in cells}
        ys = {r for _, r in cells}
        # An L-tromino: 3 cells inside a 2x2 box.
        if len(cells) != 3 or max(xs) - min(xs) != 1 or max(ys) - min(ys) != 1:
            return False
    return True


for n in range(0, 6):
    size = 2**n
    ok = all(is_valid_tiling(n, (c, r), tile(n, (c, r))) for c in range(size) for r in range(size))
    tiles = len(set(tile(n, (0, 0)).values()))
    print(f"n={n}: every Bill position tiles correctly: {ok}; tiles used: {tiles}")

# TODO: the tile counts are 0, 1, 5, 21, 85, ... Guess a formula, then prove it by induction.
# Hint: how does the count for n+1 relate to the count for n?
