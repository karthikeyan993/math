<script setup lang="ts">
// Six-people theorem (MCS §1.7): try to decide every pair without creating
// 3 people who all met (a club) or 3 who never met (strangers).
import { computed, ref } from 'vue'
import { key, monoTriangles, type Edge } from './party'

const n = ref(5)
const edges = ref<Record<string, Edge>>({})
const names = 'ABCDEF'
const R = 110, C = 140
const pos = computed(() => Array.from({ length: n.value }, (_, i) => {
  const a = -Math.PI / 2 + (2 * Math.PI * i) / n.value
  return { x: C + R * Math.cos(a), y: C + R * Math.sin(a) }
}))
const pairs = computed(() => {
  const out: [number, number][] = []
  for (let i = 0; i < n.value; i++) for (let j = i + 1; j < n.value; j++) out.push([i, j])
  return out
})
const tris = computed(() => monoTriangles(n.value, edges.value))
const decided = computed(() => pairs.value.filter(([i, j]) => edges.value[key(i, j)]).length)
const inTri = (i: number, j: number) => tris.value.some((t) => t.people.includes(i) && t.people.includes(j))

function cycle(i: number, j: number) {
  const k = key(i, j)
  const next: Record<string, Edge> = { undefined: 'met', met: 'not', not: undefined } as any
  edges.value = { ...edges.value, [k]: next[String(edges.value[k])] }
}
function setN(m: number) { n.value = m; edges.value = {} }
function pentagon() {
  setN(5)
  const e: Record<string, Edge> = {}
  pairs.value.forEach(([i, j]) => { e[key(i, j)] = (j - i) % 5 === 1 || (j - i) % 5 === 4 ? 'met' : 'not' })
  edges.value = e
}
</script>

<template>
  <div class="viz" data-viz="PartyGraph">
    <div class="viz-title">Avoid a club of 3 and avoid 3 strangers</div>
    <div class="viz-hint">Tap a line to cycle: undecided (grey) → <span class="met">met</span> → <span class="not">never met</span>. Goal: decide <b>every</b> pair without making a one-colour triangle. Try 5 people, then 6.</div>
    <div class="viz-controls">
      <button class="viz-btn" :class="{ primary: n === 5 }" @click="setN(5)">5 people</button>
      <button class="viz-btn" :class="{ primary: n === 6 }" @click="setN(6)">6 people</button>
      <button class="viz-btn" @click="edges = {}">Clear</button>
    </div>
    <svg :viewBox="`0 0 ${2 * C} ${2 * C}`" class="g">
      <g v-for="[i, j] in pairs" :key="key(i, j)" @click="cycle(i, j)" class="edge">
        <line :x1="pos[i].x" :y1="pos[i].y" :x2="pos[j].x" :y2="pos[j].y" class="hit" />
        <line :x1="pos[i].x" :y1="pos[i].y" :x2="pos[j].x" :y2="pos[j].y" :class="[edges[key(i, j)] ?? 'und', { tri: inTri(i, j) }]" />
      </g>
      <g v-for="(p, i) in pos" :key="i">
        <circle :cx="p.x" :cy="p.y" r="16" class="node" />
        <text :x="p.x" :y="p.y + 5" text-anchor="middle" class="nm">{{ names[i] }}</text>
      </g>
    </svg>
    <div class="viz-readout">
      <template v-if="tris.length">
        Found: {{ tris.map((t) => t.people.map((i) => names[i]).join('') + (t.kind === 'met' ? ' (club)' : ' (strangers)')).join(', ') }}. Change a line to break it.
      </template>
      <template v-else-if="decided === pairs.length">
        All {{ pairs.length }} pairs decided and no one-colour triangle: a counterexample for {{ n }} people!
      </template>
      <template v-else>{{ decided }} of {{ pairs.length }} pairs decided. No one-colour triangle yet.</template>
    </div>
    <details v-if="n === 5" class="peek"><summary>Stuck on 5? Show a counterexample</summary><button class="viz-btn" @click="pentagon">Load the pentagon</button></details>
  </div>
</template>

<style scoped>
.g { width: 100%; max-width: 300px; display: block; margin: 6px auto; }
.hit { stroke: transparent; stroke-width: 16; cursor: pointer; }
.edge line:not(.hit) { pointer-events: none; stroke-width: 3; }
.und { stroke: var(--viz-grid); }
.met { stroke: var(--viz-teal); color: var(--viz-teal); font-weight: 600; }
.not { stroke: var(--viz-rose); stroke-dasharray: 6 5; color: var(--viz-rose); font-weight: 600; }
.tri { stroke-width: 6 !important; }
.node { fill: var(--viz-panel); stroke: var(--viz-ink); stroke-width: 1.5; }
.nm { font-size: 14px; font-weight: 700; fill: var(--viz-ink); pointer-events: none; }
.peek { margin-top: 8px; font-size: 0.85rem; color: var(--viz-muted); }
</style>
