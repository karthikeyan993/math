// Statements for the QuantifierGame, over a small finite domain.
// The game computes truth values itself; tools/verify/components.py checks
// them against an independent Python evaluation.

export type Quant = ['A' | 'E', string]
export interface Statement {
  id: string
  text: string // shown to the learner, in Unicode
  quants: Quant[]
  pred: (env: Record<string, number>) => boolean
  lesson: string // one line shown after the reveal
}

export const DOMAIN = [0, 1, 2, 3, 4]

export const STATEMENTS: Statement[] = [
  {
    id: 'sum-AE',
    text: '∀x ∃y. x + y = 4',
    quants: [['A', 'x'], ['E', 'y']],
    pred: ({ x, y }) => x + y === 4,
    lesson: 'You pick y after seeing x, so y = 4 − x always works.',
  },
  {
    id: 'sum-EA',
    text: '∃y ∀x. x + y = 4',
    quants: [['E', 'y'], ['A', 'x']],
    pred: ({ x, y }) => x + y === 4,
    lesson: 'Same predicate, quantifiers swapped. Now you commit to y first, and one y can only match one x.',
  },
  {
    id: 'bigger-AE',
    text: '∀x ∃y. y > x',
    quants: [['A', 'x'], ['E', 'y']],
    pred: ({ x, y }) => y > x,
    lesson: 'False here, because the opponent picks x = 4 and nothing in D is bigger. Over ℕ the same formula is true. The domain is part of the meaning.',
  },
  {
    id: 'max-EA',
    text: '∃y ∀x. y ≥ x',
    quants: [['E', 'y'], ['A', 'x']],
    pred: ({ x, y }) => y >= x,
    lesson: 'True: y = 4 beats every x. So ∃∀ can be true. Swapping quantifiers changes the meaning, not necessarily the truth value.',
  },
]

// Is the statement true, given the picks so far for quants[0..depth-1]?
export function truth(s: Statement, env: Record<string, number> = {}, depth = 0): boolean {
  if (depth === s.quants.length) return s.pred(env)
  const [q, v] = s.quants[depth]
  const sub = (d: number) => truth(s, { ...env, [v]: d }, depth + 1)
  return q === 'A' ? DOMAIN.every(sub) : DOMAIN.some(sub)
}

// The opponent's ∀ pick: a value that makes the rest false, if one exists.
export function opponentPick(s: Statement, env: Record<string, number>, depth: number): number {
  const v = s.quants[depth][1]
  return DOMAIN.find((d) => !truth(s, { ...env, [v]: d }, depth + 1)) ?? DOMAIN[0]
}

// The four two-quantifier statements about a grid P[x][y] (rows x, columns y).
export function gridStatements(P: boolean[][]) {
  const xs = P.map((_, x) => x)
  const ys = P[0].map((_, y) => y)
  return {
    AxEy: xs.every((x) => ys.some((y) => P[x][y])), // every row has a dot
    EyAx: ys.some((y) => xs.every((x) => P[x][y])), // some column is full
    ExAy: xs.some((x) => ys.every((y) => P[x][y])), // some row is full
    AyEx: ys.every((y) => xs.some((x) => P[x][y])), // every column has a dot
  }
}

// A winning ∃ pick for the learner, if one exists (used for the hint after a loss).
export function winningPick(s: Statement, env: Record<string, number>, depth: number): number | null {
  const v = s.quants[depth][1]
  return DOMAIN.find((d) => truth(s, { ...env, [v]: d }, depth + 1)) ?? null
}
