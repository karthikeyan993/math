<script setup lang="ts">
import { ref, computed } from 'vue'

const n = ref(5)
const showCopy = ref(false)
const showStep = ref(false)

const MAX = 12
const cell = computed(() => Math.min(30, 300 / (n.value + 1)))
const W = computed(() => n.value * cell.value)
const H = computed(() => (n.value + 1) * cell.value)

// Column c (1..n) of the staircase has c cells, stacked from the bottom.
const stairs = computed(() => {
  const out: { x: number; y: number; last: boolean }[] = []
  for (let c = 1; c <= n.value; c++)
    for (let r = 0; r < c; r++) out.push({ x: (c - 1) * cell.value, y: H.value - (r + 1) * cell.value, last: c === n.value })
  return out
})
// The flipped copy: column c has n+1-c cells, hanging from the top.
const copy = computed(() => {
  const out: { x: number; y: number }[] = []
  for (let c = 1; c <= n.value; c++)
    for (let r = 0; r < n.value + 1 - c; r++) out.push({ x: (c - 1) * cell.value, y: r * cell.value })
  return out
})
const total = computed(() => (n.value * (n.value + 1)) / 2)
const sumText = computed(() => {
  const terms = Array.from({ length: n.value }, (_, i) => i + 1)
  return terms.length > 8 ? `1 + 2 + … + ${n.value}` : terms.join(' + ')
})
</script>

<template>
  <div class="viz">
    <div class="viz-title">Why 1 + 2 + ⋯ + n = n(n+1)/2</div>
    <div class="viz-hint">The staircase has 1 + 2 + ⋯ + n blocks. Add a flipped copy and see what shape you get.</div>
    <div class="stage">
      <svg :viewBox="`-4 -4 ${W + 8} ${H + 8}`" :style="{ maxWidth: `${W + 8}px` }">
        <g class="copy" :class="{ on: showCopy }">
          <rect v-for="(b, i) in copy" :key="'c' + i" :x="b.x + 1" :y="b.y + 1" :width="cell - 2" :height="cell - 2" rx="3" fill="var(--viz-gold)" opacity="0.85" />
        </g>
        <rect
          v-for="(b, i) in stairs"
          :key="'s' + i"
          :x="b.x + 1"
          :y="b.y + 1"
          :width="cell - 2"
          :height="cell - 2"
          rx="3"
          :fill="showStep && b.last ? 'var(--viz-rose)' : 'var(--viz-blue)'"
        />
        <rect v-if="showCopy" x="0" y="0" :width="W" :height="H" fill="none" stroke="var(--viz-ink)" stroke-dasharray="4 4" />
      </svg>
    </div>
    <div class="viz-controls">
      <label>n = {{ n }} <input v-model.number="n" type="range" min="1" :max="MAX" /></label>
      <button class="viz-btn primary" @click="showCopy = !showCopy">{{ showCopy ? 'Remove copy' : 'Add a flipped copy' }}</button>
      <label><input v-model="showStep" type="checkbox" /> Highlight the step from n−1 to n</label>
    </div>
    <div class="viz-readout">
      <template v-if="showCopy">
        Two staircases make an <b>{{ n }} × {{ n + 1 }}</b> rectangle = {{ n * (n + 1) }} blocks, so one staircase is
        {{ n * (n + 1) }} / 2 = <b>{{ total }}</b>.
      </template>
      <template v-else-if="showStep">
        The step from n−1 to n adds one column of <b>{{ n }}</b> blocks. That's the "+ (n+1)" you see in the inductive step.
      </template>
      <template v-else>{{ sumText }} = <b>{{ total }}</b></template>
    </div>
  </div>
</template>

<style scoped>
.stage { display: flex; justify-content: center; }
.copy { opacity: 0; transform: translateY(-30px); transition: opacity 0.4s, transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1); }
.copy.on { opacity: 1; transform: translateY(0); }
</style>
