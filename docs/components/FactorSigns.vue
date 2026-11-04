<script setup lang="ts">
// Theorem 1.5.1 (MCS p. 12): drag x and watch the signs of the three factors.
import { computed, ref } from 'vue'
import { cubic } from './numbers'

const x = ref(-1.5)
const W = 320, H = 200, X0 = -3, X1 = 3, Y0 = -16, Y1 = 18
const sx = (v: number) => ((v - X0) / (X1 - X0)) * W
const sy = (v: number) => H - ((v - Y0) / (Y1 - Y0)) * H
const path = computed(() => {
  const pts: string[] = []
  for (let i = 0; i <= 120; i++) {
    const v = X0 + ((X1 - X0) * i) / 120
    pts.push(`${i ? 'L' : 'M'}${sx(v).toFixed(1)},${sy(cubic(v)).toFixed(1)}`)
  }
  return pts.join(' ')
})
const factors = computed(() => [
  { label: 'x', v: x.value },
  { label: '2 − x', v: 2 - x.value },
  { label: '2 + x', v: 2 + x.value },
])
const product = computed(() => x.value * (2 - x.value) * (2 + x.value))
const negatives = computed(() => factors.value.filter((f) => f.v < 0).length)
const fmt = (v: number) => (Math.abs(v) < 0.005 ? '0.00' : v.toFixed(2))
</script>

<template>
  <div class="viz" data-viz="FactorSigns">
    <div class="viz-title">Why does the hypothesis 0 ≤ x ≤ 2 matter?</div>
    <div class="viz-hint">Drag x. The shaded band is the hypothesis. Find where the curve dips below zero, then see which factor went negative.</div>
    <svg :viewBox="`0 0 ${W} ${H}`" class="plot">
      <rect :x="sx(0)" y="0" :width="sx(2) - sx(0)" :height="H" class="band" />
      <line :x1="0" :y1="sy(0)" :x2="W" :y2="sy(0)" class="axis" />
      <line :x1="sx(0)" y1="0" :x2="sx(0)" :y2="H" class="axis" />
      <text :x="sx(1)" y="14" class="lbl" text-anchor="middle">0 ≤ x ≤ 2</text>
      <path :d="path" class="curve" />
      <circle :cx="sx(x)" :cy="sy(cubic(x))" r="5" :class="cubic(x) > 0 ? 'pos' : 'neg'" />
    </svg>
    <div class="viz-controls">
      <label>x = {{ fmt(x) }} <input v-model.number="x" type="range" :min="X0" :max="X1" step="0.05" /></label>
    </div>
    <div class="chips">
      <span v-for="f in factors" :key="f.label" class="chip" :class="f.v >= 0 ? 'pos' : 'neg'">{{ f.label }} = {{ fmt(f.v) }}</span>
    </div>
    <div class="viz-readout">
      x(2 − x)(2 + x) = {{ fmt(product) }}, so −x³ + 4x + 1 = {{ fmt(product) }} + 1 = <b>{{ fmt(cubic(x)) }}</b>
      <br />
      <template v-if="negatives === 0">All three factors are ≥ 0 (that's exactly the band), so the product is ≥ 0 and the total is ≥ 1. That's the whole proof.</template>
      <template v-else-if="negatives === 1">One factor is negative, so the product is ≤ 0. The proof's argument breaks here, and the total can drop below 0.</template>
      <template v-else>Two factors are negative, so the product is positive again and the total is above 0. The conclusion holds here even though the hypothesis is false. Outside the hypothesis, the theorem simply says nothing.</template>
    </div>
  </div>
</template>

<style scoped>
.plot { width: 100%; max-width: 420px; display: block; margin: 8px auto; }
.band { fill: color-mix(in srgb, var(--viz-teal) 14%, transparent); }
.axis { stroke: var(--viz-grid); stroke-width: 1.5; }
.curve { fill: none; stroke: var(--viz-blue); stroke-width: 2.5; }
.lbl { font-size: 11px; fill: var(--viz-muted); }
circle.pos { fill: var(--viz-teal); }
circle.neg { fill: var(--viz-rose); }
.chips { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin: 6px 0; }
.chip { padding: 3px 10px; border-radius: 999px; font-size: 0.85rem; font-variant-numeric: tabular-nums; border: 1px solid; }
.chip.pos { border-color: var(--viz-teal); background: color-mix(in srgb, var(--viz-teal) 14%, transparent); }
.chip.neg { border-color: var(--viz-rose); background: color-mix(in srgb, var(--viz-rose) 18%, transparent); }
</style>
