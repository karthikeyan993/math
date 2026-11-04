<script setup lang="ts">
import { ref, computed, onBeforeUnmount } from 'vue'

const N = 12
const baseCase = ref(true)
const stepHolds = ref(true)
const gapAfter = ref(6) // when the step fails, domino k does not reach k+1
const fallen = ref<boolean[]>(Array(N).fill(false))
const running = ref(false)
const done = ref(false)
let timers: number[] = []

function clear() {
  timers.forEach((t) => clearTimeout(t))
  timers = []
}
function reset() {
  clear()
  fallen.value = Array(N).fill(false)
  running.value = false
  done.value = false
}
function run() {
  reset()
  running.value = true
  let last = -1
  if (baseCase.value) {
    last = stepHolds.value ? N - 1 : gapAfter.value
  }
  for (let i = 0; i <= last; i++) {
    timers.push(
      window.setTimeout(() => {
        const f = fallen.value.slice()
        f[i] = true
        fallen.value = f
      }, 180 * i),
    )
  }
  timers.push(
    window.setTimeout(() => {
      running.value = false
      done.value = true
    }, 180 * Math.max(last + 1, 1) + 300),
  )
}
onBeforeUnmount(clear)

const spacing = 52
const W = spacing * N + 30
const H = 130
const dx = (i: number) => 22 + i * spacing
// When the step fails at k, push domino k+1 further away so the gap is visible.
const xOf = (i: number) => dx(i) + (!stepHolds.value && i > gapAfter.value ? 18 : 0)

const message = computed(() => {
  if (!done.value) return ''
  if (!baseCase.value)
    return 'Nothing fell. Every domino would knock the next one over, but nobody pushed the first. The inductive step without a base case proves nothing.'
  if (!stepHolds.value)
    return `Dominoes 0 to ${gapAfter.value} fell, then the chain stopped. P(${gapAfter.value}) does not lead to P(${gapAfter.value + 1}), so we learn nothing about anything after it. The step has to hold for every n, not most of them.`
  return 'All of them fell. With these two rules this would work for a million dominoes or more: every domino falls.'
})
</script>

<template>
  <div class="viz">
    <div class="viz-title">Two rules knock over every domino</div>
    <div class="viz-hint">Domino n stands for the claim P(n). "Falls" means "is proved". Switch a rule off, then press Push.</div>
    <svg :viewBox="`0 0 ${W} ${H}`" role="img" aria-label="A row of dominoes">
      <line :x1="0" :x2="W" :y1="100" :y2="100" stroke="var(--viz-grid)" stroke-width="2" />
      <g v-for="i in N" :key="i">
        <rect
          :x="xOf(i - 1)"
          y="40"
          width="12"
          height="60"
          rx="2"
          class="domino"
          :class="{ down: fallen[i - 1] }"
          :fill="fallen[i - 1] ? 'var(--viz-blue)' : 'var(--viz-muted)'"
        />
        <text :x="xOf(i - 1) + 6" y="122" text-anchor="middle" class="lbl">P({{ i - 1 }})</text>
      </g>
      <g v-if="baseCase">
        <path :d="`M ${dx(0) - 18} 52 l 12 0`" stroke="var(--viz-gold)" stroke-width="3" marker-end="url(#arrow)" />
      </g>
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto">
          <path d="M0,0 L10,5 L0,10 z" fill="var(--viz-gold)" />
        </marker>
      </defs>
    </svg>
    <div class="viz-controls">
      <label><input v-model="baseCase" type="checkbox" @change="reset" /> Base case: P(0) is true (someone pushes domino 0)</label>
      <label><input v-model="stepHolds" type="checkbox" @change="reset" /> Inductive step: P(n) ⇒ P(n+1) for <i>every</i> n</label>
      <label v-if="!stepHolds">
        the step fails at n = {{ gapAfter }}
        <input v-model.number="gapAfter" type="range" min="0" :max="N - 2" @input="reset" />
      </label>
      <button class="viz-btn primary" :disabled="running" @click="run">Push</button>
      <button class="viz-btn" @click="reset">Stand them up</button>
    </div>
    <div class="viz-readout">{{ message }}</div>
  </div>
</template>

<style scoped>
.domino {
  transform-box: fill-box;
  transform-origin: 100% 100%;
  transition: transform 0.22s ease-in, fill 0.22s;
}
.domino.down { transform: rotate(62deg); }
.lbl { font-size: 11px; fill: var(--viz-muted); font-family: var(--vp-font-family-mono); }
</style>
