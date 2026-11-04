<script setup lang="ts">
// Predict whether two formulas are equivalent, then see the truth table with
// the disagreeing rows highlighted. Editable afterwards, as a sandbox.
// Evaluation is done by logic.ts (cross-checked by tools/verify/components.py).
import { computed, ref } from 'vue'
import { evaluate, parse, rows, variables } from './logic'

const props = defineProps<{ left: string; right: string }>()
const left = ref(props.left)
const right = ref(props.right)
const guess = ref<boolean | null>(null)

const result = computed(() => {
  try {
    const f = parse(left.value), g = parse(right.value)
    const vars = variables(f, variables(g))
    const rs = rows(vars).map((env) => ({ env, a: evaluate(f, env), b: evaluate(g, env) }))
    return { vars, rs, equiv: rs.every((r) => r.a === r.b), error: null as string | null }
  } catch (e) {
    return { vars: [], rs: [], equiv: false, error: (e as Error).message }
  }
})
const tf = (b: boolean) => (b ? 'T' : 'F')
</script>

<template>
  <div class="viz" data-viz="EquivalenceChecker">
    <div class="viz-title">Equivalent or not?</div>
    <div class="forms">
      <input v-model="left" :disabled="guess === null" aria-label="left formula" />
      <span class="vs">vs</span>
      <input v-model="right" :disabled="guess === null" aria-label="right formula" />
    </div>
    <div v-if="guess === null" class="viz-controls">
      <span>Predict first:</span>
      <button class="viz-btn" @click="guess = true">Equivalent</button>
      <button class="viz-btn" @click="guess = false">Not equivalent</button>
    </div>
    <template v-else>
      <p v-if="result.error" class="err">{{ result.error }}</p>
      <template v-else>
        <div class="wrap">
          <table>
            <thead><tr><th v-for="v in result.vars" :key="v" class="var">{{ v }}</th><th>left</th><th>right</th></tr></thead>
            <tbody>
              <tr v-for="(r, i) in result.rs" :key="i" :class="{ diff: r.a !== r.b }">
                <td v-for="v in result.vars" :key="v" class="var">{{ tf(r.env[v]) }}</td>
                <td>{{ tf(r.a) }}</td><td>{{ tf(r.b) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="viz-readout">
          <b>{{ result.equiv ? 'Equivalent' : 'Not equivalent' }}</b>:
          {{ result.equiv ? 'the columns match on every row.' : 'they disagree on the highlighted rows. Each one is a counterexample.' }}
          <span v-if="guess !== null && left === props.left && right === props.right">You predicted {{ guess ? 'equivalent' : 'not equivalent' }}{{ guess === result.equiv ? ' ✓' : ' ✗' }}.</span>
          <br /><span class="tip">Now edit either formula and watch the table change. Words: NOT, AND, OR, XOR, IMPLIES, IFF, and parentheses.</span>
        </div>
      </template>
    </template>
  </div>
</template>

<style scoped>
.forms { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin: 8px 0; }
.forms input { flex: 1 1 200px; padding: 6px 8px; border: 1px solid var(--viz-grid); border-radius: 8px; background: var(--viz-panel); color: var(--viz-ink); font-family: var(--vp-font-family-mono); font-size: 0.85rem; }
.vs { color: var(--viz-muted); font-size: 0.85rem; }
.wrap { overflow-x: auto; }
table { border-collapse: collapse; margin: 8px auto; }
th, td { border: 1px solid var(--viz-grid); padding: 3px 10px; text-align: center; font-size: 0.85rem; }
.var { color: var(--viz-muted); }
tr.diff td { background: color-mix(in srgb, var(--viz-rose) 18%, transparent); font-weight: 700; }
.err { color: var(--viz-rose); font-size: 0.85rem; }
.tip { color: var(--viz-muted); font-size: 0.8rem; }
</style>
