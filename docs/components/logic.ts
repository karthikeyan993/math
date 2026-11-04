// Propositional formulas in the textbook's word notation (MCS §3.1):
//   NOT, AND, OR, XOR, IMPLIES, IFF, parentheses, and variable names.
//
// Deliberately strict, so a formula can't silently mean something else:
// NOT applies to the single atom after it (write NOT(A AND B) for more), and
// one parenthesis level may not mix different binary operators or chain
// IMPLIES or IFF. Write (P AND Q) OR R, not P AND Q OR R.
//
// tools/verify/_logic.py is an independent Python copy of this grammar;
// tools/verify/components.py checks that the two agree on every formula
// used in a lesson.

export type Op = 'AND' | 'OR' | 'XOR' | 'IMPLIES' | 'IFF'
export type Formula =
  | { k: 'var'; name: string }
  | { k: 'not'; a: Formula }
  | { k: 'bin'; op: Op; args: Formula[] }

const OPS = new Set<string>(['AND', 'OR', 'XOR', 'IMPLIES', 'IFF'])
const TOKEN = /\(|\)|[A-Za-z_][A-Za-z0-9_]*/g

export function parse(src: string): Formula {
  if (src.replace(TOKEN, '').trim() !== '') throw new Error(`bad character in formula: ${src}`)
  const toks = src.match(TOKEN) ?? []
  let i = 0

  function atom(): Formula {
    const t = toks[i++]
    if (t === undefined) throw new Error(`formula ends early: ${src}`)
    if (t === 'NOT') return { k: 'not', a: atom() }
    if (t === '(') {
      const e = level()
      if (toks[i++] !== ')') throw new Error(`missing ) in: ${src}`)
      return e
    }
    if (t === ')' || OPS.has(t)) throw new Error(`unexpected ${t} in: ${src}`)
    return { k: 'var', name: t }
  }

  function level(): Formula {
    const args = [atom()]
    let op: Op | null = null
    while (i < toks.length && OPS.has(toks[i])) {
      const next = toks[i++] as Op
      if (op && next !== op) throw new Error(`mixes ${op} and ${next} without parentheses: ${src}`)
      if ((next === 'IMPLIES' || next === 'IFF') && op) throw new Error(`chained ${next} needs parentheses: ${src}`)
      op = next
      args.push(atom())
    }
    return op ? { k: 'bin', op, args } : args[0]
  }

  const f = level()
  if (i !== toks.length) throw new Error(`unexpected ${toks[i]} in: ${src}`)
  return f
}

export function evaluate(f: Formula, env: Record<string, boolean>): boolean {
  switch (f.k) {
    case 'var':
      if (!(f.name in env)) throw new Error(`no value for ${f.name}`)
      return env[f.name]
    case 'not':
      return !evaluate(f.a, env)
    case 'bin': {
      const v = f.args.map((a) => evaluate(a, env))
      switch (f.op) {
        case 'AND': return v.every(Boolean)
        case 'OR': return v.some(Boolean)
        case 'XOR': return v.filter(Boolean).length % 2 === 1
        case 'IFF': return v[0] === v[1]
        case 'IMPLIES': return !v[0] || v[1]
      }
    }
  }
}

export function variables(f: Formula, out: string[] = []): string[] {
  if (f.k === 'var') { if (!out.includes(f.name)) out.push(f.name) }
  else if (f.k === 'not') variables(f.a, out)
  else f.args.forEach((a) => variables(a, out))
  return out
}

// Rows in textbook order: T before F, first variable changes slowest.
export function rows(vars: string[]): Record<string, boolean>[] {
  const n = vars.length
  return Array.from({ length: 2 ** n }, (_, r) =>
    Object.fromEntries(vars.map((v, j) => [v, ((r >> (n - 1 - j)) & 1) === 0])),
  )
}

// Truth table of each column formula as a T/F string, e.g. "TFTT".
export function table(vars: string[], columns: string[]): string[] {
  const fs = columns.map(parse)
  return fs.map((f) => rows(vars).map((env) => (evaluate(f, env) ? 'T' : 'F')).join(''))
}
