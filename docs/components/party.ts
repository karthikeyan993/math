// Six-people theorem (MCS §1.7, p. 15) as a graph: people are vertices, and
// each pair is 'met', 'not' (never met) or undecided. Cross-checked by
// tools/verify/components.py against an independent Python version.

export type Edge = 'met' | 'not' | undefined
export const key = (i: number, j: number) => (i < j ? `${i}-${j}` : `${j}-${i}`)

// Every triangle whose three edges are all decided and all the same.
export function monoTriangles(n: number, edges: Record<string, Edge>): { people: number[]; kind: 'met' | 'not' }[] {
  const out: { people: number[]; kind: 'met' | 'not' }[] = []
  for (let a = 0; a < n; a++)
    for (let b = a + 1; b < n; b++)
      for (let c = b + 1; c < n; c++) {
        const e = [edges[key(a, b)], edges[key(a, c)], edges[key(b, c)]]
        if (e[0] && e[0] === e[1] && e[1] === e[2]) out.push({ people: [a, b, c], kind: e[0] })
      }
  return out
}
