// Small number helpers for the visuals. Cross-checked by tools/verify/components.py.

export function isPrime(n: number): boolean {
  if (n < 2) return false
  for (let d = 2; d * d <= n; d++) if (n % d === 0) return false
  return true
}

// Smallest prime factorisation, e.g. 1681 -> [41, 41].
export function factor(n: number): number[] {
  const out: number[] = []
  let m = n
  for (let d = 2; d * d <= m; d++) while (m % d === 0) { out.push(d); m /= d }
  if (m > 1) out.push(m)
  return out
}

// MCS §1.1 (p. 5): p(n) ::= n^2 + n + 41.
export const euler = (n: number) => n * n + n + 41

// MCS Theorem 1.5.1 (p. 12): f(x) = -x^3 + 4x + 1 = x(2 - x)(2 + x) + 1.
export const cubic = (x: number) => -(x ** 3) + 4 * x + 1
