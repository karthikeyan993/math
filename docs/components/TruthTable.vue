<script setup lang="ts">
// Fill-in truth table. The answers are computed from the formulas by logic.ts,
// never typed by hand, so the table can't contain a wrong "answer key".
// Usage: <TruthTable vars="P,Q" cols="P IMPLIES Q; Q IMPLIES P" title="..." />
// Columns listed in `given` (by number, 1-based, e.g. given="1") start filled in.
import { computed, ref } from 'vue'
import { rows, table } from './logic'

const props = defineProps<{ vars: string; cols: string; title?: string; given?: string }>()
const vars = computed(() => props.vars.split(',').map((s) => s.trim()))
const cols = computed(() => props.cols.split(';').map((s) => s.trim()))
const answers = computed(() => table(vars.value, cols.value))
const envs = computed(() => rows(vars.value))
const givenCols = computed(() => new Set((props.given ?? '').split(',').filter(Boolean).map((s) => Number(s) - 1)))

const cells = ref<string[][]>(cols.value.map((_, c) =>
  envs.value.map((_, r) => (givenCols.value.has(c) ? answers.value[c][r] : '')),
))
const checked = ref(false)
const revealed = ref(false)

function cycle(c: number, r: number) {
  if (givenCols.value.has(c) || revealed.value) return
  const order = ['', 'T', 'F']
  cells.value[c][r] = order[(order.indexOf(cells.value[c][r]) + 1) % 3]
  checked.value = false
}
const wrong = computed(() => {
  let n = 0
  cols.value.forEach((_, c) => envs.value.forEach((_, r) => { if (cells.value[c][r] !== answers.value[c][r]) n++ }))
  return n
})
const allRight = computed(() => wrong.value === 0)
function reveal() {
  cells.value = answers.value.map((s) => s.split(''))
  revealed.value = true
  checked.value = true
}
function state(c: number, r: number) {
  if (!checked.value || givenCols.value.has(c)) return ''
  return cells.value[c][r] === answers.value[c][r] ? 'ok' : 'bad'
}
</script>

<template>
  <div class="viz" data-viz="TruthTable">
    <div class="viz-title">{{ title ?? 'Fill in the truth table' }}</div>
    <div class="viz-hint">Tap a cell to cycle blank → T → F. Fill every blank cell, then check.</div>
    <div class="wrap">
      <table>
        <thead>
          <tr>
            <th v-for="v in vars" :key="v" class="var">{{ v }}</th>
            <th v-for="(c, i) in cols" :key="i">{{ c }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(env, r) in envs" :key="r">
            <td v-for="v in vars" :key="v" class="var">{{ env[v] ? 'T' : 'F' }}</td>
            <td v-for="(_, c) in cols" :key="c">
              <button
                class="cell"
                :class="[state(c, r), { given: givenCols.has(c) }]"
                :aria-label="`row ${r + 1}, column ${cols[c]}`"
                @click="cycle(c, r)"
              >{{ cells[c][r] || '·' }}</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="viz-controls">
      <button class="viz-btn primary" :disabled="revealed" @click="checked = true">Check</button>
      <button class="viz-btn" :disabled="revealed" @click="reveal">Show the answer</button>
    </div>
    <div v-if="checked" class="viz-readout">
      <template v-if="allRight && !revealed">All correct.</template>
      <template v-else-if="revealed">Here's the full table. Compare it with yours before reading on.</template>
      <template v-else>{{ wrong }} cell{{ wrong === 1 ? '' : 's' }} wrong or blank (marked red). Fix them and check again.</template>
    </div>
    <div v-if="checked && allRight" class="after"><slot /></div>
  </div>
</template>

<style scoped>
.wrap { overflow-x: auto; }
table { border-collapse: collapse; margin: 8px auto; font-variant-numeric: tabular-nums; }
th, td { border: 1px solid var(--viz-grid); padding: 4px 8px; text-align: center; font-size: 0.85rem; }
th { font-weight: 600; white-space: nowrap; }
.var { color: var(--viz-muted); }
.cell { min-width: 2.2em; min-height: 2em; border: 1px solid var(--viz-grid); border-radius: 6px; background: var(--viz-panel); color: var(--viz-ink); font: inherit; font-weight: 700; cursor: pointer; }
.cell.given { cursor: default; color: var(--viz-muted); border-style: dashed; }
.cell.ok { border-color: var(--viz-teal); background: color-mix(in srgb, var(--viz-teal) 15%, transparent); }
.cell.bad { border-color: var(--viz-rose); background: color-mix(in srgb, var(--viz-rose) 15%, transparent); }
.after { margin-top: 10px; border-top: 1px dashed var(--viz-grid); padding-top: 8px; }
.after :deep(p) { margin: 6px 0; }
</style>
