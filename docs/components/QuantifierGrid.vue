<script setup lang="ts">
// A predicate P(x, y) on a 5 × 5 domain drawn as a grid of dots.
// ∀x∃y = every row has a dot; ∃y∀x = some column is full; and so on.
import { computed, ref } from 'vue'
import { gridStatements } from './quantifiers'

const D = [0, 1, 2, 3, 4]
const make = (f: (x: number, y: number) => boolean) => D.map((x) => D.map((y) => f(x, y)))
const P = ref<boolean[][]>(make((x, y) => x === y))
const presets: [string, (x: number, y: number) => boolean][] = [
  ['x = y', (x, y) => x === y],
  ['x + y = 4', (x, y) => x + y === 4],
  ['y > x', (x, y) => y > x],
  ['y ≥ x', (x, y) => y >= x],
  ['empty', () => false],
]
const st = computed(() => gridStatements(P.value))
const focus = ref<string | null>(null)
const challenge = computed(() => st.value.AxEy && !st.value.EyAx)

function toggle(x: number, y: number) {
  const g = P.value.map((r) => [...r])
  g[x][y] = !g[x][y]
  P.value = g
}
// Rows/columns to highlight for the statement under the pointer.
function mark(x: number, y: number): string {
  const rowFull = (r: number) => D.every((c) => P.value[r][c])
  const rowEmpty = (r: number) => D.every((c) => !P.value[r][c])
  const colFull = (c: number) => D.every((r) => P.value[r][c])
  const colEmpty = (c: number) => D.every((r) => !P.value[r][c])
  switch (focus.value) {
    case 'AxEy': return rowEmpty(x) ? 'bad' : ''
    case 'EyAx': return colFull(y) ? 'good' : ''
    case 'ExAy': return rowFull(x) ? 'good' : ''
    case 'AyEx': return colEmpty(y) ? 'bad' : ''
  }
  return ''
}
const rowsOf = [
  { k: 'AxEy', f: '∀x ∃y. P(x, y)', say: 'every row has at least one dot' },
  { k: 'EyAx', f: '∃y ∀x. P(x, y)', say: 'some column is completely full' },
  { k: 'ExAy', f: '∃x ∀y. P(x, y)', say: 'some row is completely full' },
  { k: 'AyEx', f: '∀y ∃x. P(x, y)', say: 'every column has at least one dot' },
] as const
</script>

<template>
  <div class="viz" data-viz="QuantifierGrid">
    <div class="viz-title">Quantifiers are row and column checks</div>
    <div class="viz-hint">Row x, column y. A dot means P(x, y) is true. Tap cells to toggle. Hover or tap a statement to see what it looks at.</div>
    <div class="viz-controls">
      <span>Load:</span>
      <button v-for="[name, f] in presets" :key="name" class="viz-btn" @click="P = make(f)">{{ name }}</button>
    </div>
    <div class="layout">
      <div class="board">
        <div class="corner">x \ y</div>
        <div v-for="y in D" :key="'h' + y" class="head">{{ y }}</div>
        <template v-for="x in D" :key="'r' + x">
          <div class="head">{{ x }}</div>
          <button v-for="y in D" :key="y" class="sq" :class="mark(x, y)" :aria-label="`P(${x}, ${y})`" @click="toggle(x, y)">
            <span v-if="P[x][y]" class="dot" />
          </button>
        </template>
      </div>
      <ul class="stmts">
        <li v-for="r in rowsOf" :key="r.k" :class="{ on: focus === r.k }" @mouseenter="focus = r.k" @mouseleave="focus = null" @click="focus = focus === r.k ? null : r.k">
          <code>{{ r.f }}</code> <b :class="st[r.k] ? 't' : 'f'">{{ st[r.k] ? 'true' : 'false' }}</b>
          <div class="say">{{ r.say }}</div>
        </li>
      </ul>
    </div>
    <div class="viz-readout">
      Challenge: make <code>∀x ∃y</code> true but <code>∃y ∀x</code> false.
      <b v-if="challenge"> Done. Every row has a dot, but no single column serves them all.</b>
    </div>
  </div>
</template>

<style scoped>
.layout { display: flex; gap: 16px; flex-wrap: wrap; align-items: flex-start; justify-content: center; margin: 8px 0; }
.board { display: grid; grid-template-columns: repeat(6, 36px); gap: 3px; }
.corner, .head { font-size: 0.75rem; color: var(--viz-muted); display: flex; align-items: center; justify-content: center; }
.sq { width: 36px; height: 36px; border: 1px solid var(--viz-grid); border-radius: 6px; background: var(--viz-panel); cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; }
.sq.good { background: color-mix(in srgb, var(--viz-teal) 25%, transparent); border-color: var(--viz-teal); }
.sq.bad { background: color-mix(in srgb, var(--viz-rose) 25%, transparent); border-color: var(--viz-rose); }
.dot { width: 14px; height: 14px; border-radius: 50%; background: var(--viz-blue); }
.stmts { list-style: none; padding: 0; margin: 0; flex: 1 1 220px; }
.stmts li { padding: 6px 8px; border-radius: 8px; cursor: pointer; border: 1px solid transparent; margin-bottom: 4px; }
.stmts li.on { border-color: var(--viz-grid); background: var(--viz-panel); }
.say { font-size: 0.8rem; color: var(--viz-muted); }
.t { color: var(--viz-teal); }
.f { color: var(--viz-rose); }
</style>
