<script setup lang="ts">
// "Keep running tests": reveal p(n) = n² + n + 41 one n at a time.
import { computed, ref } from 'vue'
import { euler, factor, isPrime } from './numbers'

const N = 60
const bet = ref<number | null>(null)
const betInput = ref(10)
const shown = ref(0) // how many n have been tested
const firstFail = computed(() => Array.from({ length: N }, (_, n) => n).find((n) => !isPrime(euler(n))) ?? null)
const failed = computed(() => firstFail.value !== null && shown.value > firstFail.value)
const cells = computed(() => Array.from({ length: N }, (_, n) => ({ n, v: euler(n), prime: isPrime(euler(n)), on: n < shown.value })))
const last = computed(() => (shown.value ? cells.value[shown.value - 1] : null))

function run(k: number) {
  for (let i = 0; i < k && shown.value < N; i++) {
    shown.value++
    if (!isPrime(euler(shown.value - 1)) && k > 1) break // stop a batch at the first failure
  }
}
</script>

<template>
  <div class="viz" data-viz="PrimeStreak">
    <div class="viz-title">Run the tests: is n² + n + 41 always prime?</div>
    <div v-if="bet === null" class="viz-controls">
      <span>Before you start: after how many passing tests would you bet the claim is true for <b>every</b> n?</span>
      <input v-model.number="betInput" type="number" min="1" max="1000" class="num" />
      <button class="viz-btn primary" @click="bet = betInput">Lock in my bet</button>
    </div>
    <template v-else>
      <div class="grid">
        <div v-for="c in cells" :key="c.n" class="cell" :class="{ on: c.on, prime: c.on && c.prime, bad: c.on && !c.prime }" :title="c.on ? `p(${c.n}) = ${c.v}` : ''">
          <span class="n">{{ c.n }}</span>
          <span v-if="c.on" class="v">{{ c.prime ? '✓' : '✗' }}</span>
        </div>
      </div>
      <div class="viz-controls">
        <button class="viz-btn primary" :disabled="shown >= N" @click="run(1)">Run next test</button>
        <button class="viz-btn" :disabled="shown >= N" @click="run(10)">Run 10</button>
        <button class="viz-btn" @click="shown = 0">Reset</button>
      </div>
      <div class="viz-readout">
        <template v-if="last">p({{ last.n }}) = {{ last.v }} {{ last.prime ? 'is prime.' : `= ${factor(last.v).join(' × ')}, not prime.` }}</template>
        <template v-else>No tests run yet. Your bet: {{ bet }} passing tests.</template>
      </div>
      <p v-if="failed" class="verdict">
        {{ firstFail }} tests in a row passed. Test {{ firstFail! + 1 }} (n = {{ firstFail }}) failed.
        <template v-if="bet! <= firstFail!">You'd have bet after {{ bet }}, and lost.</template>
        <template v-else>Your bet of {{ bet }} would have survived this one, but no finite number of tests proves a claim about every n.</template>
        Keep running: after n = 40, failures keep turning up.
      </p>
    </template>
  </div>
</template>

<style scoped>
.num { width: 5em; padding: 4px 6px; border: 1px solid var(--viz-grid); border-radius: 6px; background: var(--viz-panel); color: var(--viz-ink); font: inherit; }
.grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 4px; margin: 10px 0; }
.cell { aspect-ratio: 1; border: 1px solid var(--viz-grid); border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 0.7rem; color: var(--viz-muted); }
.cell.prime { background: color-mix(in srgb, var(--viz-teal) 22%, transparent); border-color: var(--viz-teal); color: var(--viz-ink); }
.cell.bad { background: color-mix(in srgb, var(--viz-rose) 28%, transparent); border-color: var(--viz-rose); color: var(--viz-ink); }
.v { font-weight: 700; font-size: 0.85rem; }
.verdict { margin: 8px 0 0; font-weight: 500; }
</style>
