<script setup lang="ts">
import { ref, computed } from 'vue'

const n = ref(4)
const hovered = ref<number | null>(null)
const colors = ['var(--viz-blue)', 'var(--viz-teal)', 'var(--viz-violet)', 'var(--viz-rose)', 'var(--viz-gold)']
const cell = computed(() => Math.min(34, 280 / n.value))
const cells = computed(() => {
  const out: { x: number; y: number; shell: number }[] = []
  for (let r = 0; r < n.value; r++)
    for (let c = 0; c < n.value; c++) out.push({ x: c * cell.value, y: (n.value - 1 - r) * cell.value, shell: Math.max(r, c) })
  return out
})
const odds = computed(() => Array.from({ length: n.value }, (_, k) => 2 * k + 1))
</script>

<template>
  <div class="viz">
    <div class="viz-title">Odd numbers stack into squares</div>
    <div class="viz-hint">Each L-shaped layer is the next odd number. Hover over a layer to see its size.</div>
    <div class="stage">
      <svg :viewBox="`-2 -2 ${n * cell + 4} ${n * cell + 4}`" :style="{ maxWidth: `${n * cell + 4}px` }">
        <rect
          v-for="(b, i) in cells"
          :key="i"
          :x="b.x + 1"
          :y="b.y + 1"
          :width="cell - 2"
          :height="cell - 2"
          rx="3"
          :fill="colors[b.shell % colors.length]"
          :opacity="hovered === null || hovered === b.shell ? 0.9 : 0.25"
          @mouseenter="hovered = b.shell"
          @mouseleave="hovered = null"
        />
      </svg>
    </div>
    <div class="viz-controls">
      <label>n = {{ n }} <input v-model.number="n" type="range" min="1" max="10" /></label>
    </div>
    <div class="viz-readout">
      <template v-if="hovered !== null">Layer {{ hovered + 1 }} has 2·{{ hovered + 1 }} − 1 = <b>{{ 2 * hovered + 1 }}</b> blocks.</template>
      <template v-else>{{ odds.join(' + ') }} = <b>{{ n * n }}</b> = {{ n }}²</template>
    </div>
  </div>
</template>

<style scoped>
.stage { display: flex; justify-content: center; }
rect { transition: opacity 0.15s; cursor: pointer; }
</style>
