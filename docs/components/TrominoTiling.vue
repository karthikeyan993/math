<script setup lang="ts">
import { ref, computed, watch, onBeforeUnmount } from 'vue'

type Cell = [number, number] // [col, row]
interface Step {
  frame: { x: number; y: number; size: number }
  cells: Cell[]
  depth: number
}

const n = ref(3)
const size = computed(() => 2 ** n.value)
const bill = ref<Cell>([3, 3])
const shown = ref(0) // how many tiles are placed
const playing = ref(false)
let timer: number | undefined

// The proof's inductive step, run as a recursive algorithm.
function solve(x: number, y: number, s: number, b: Cell, depth: number, out: Step[]) {
  if (s === 1) return // base case: Bill fills the whole 1x1 courtyard
  const h = s / 2
  const cx = x + h
  const cy = y + h
  const quads = [
    { x, y, centre: [cx - 1, cy - 1] as Cell },
    { x: cx, y, centre: [cx, cy - 1] as Cell },
    { x, y: cy, centre: [cx - 1, cy] as Cell },
    { x: cx, y: cy, centre: [cx, cy] as Cell },
  ]
  const billQ = quads.findIndex((q) => b[0] >= q.x && b[0] < q.x + h && b[1] >= q.y && b[1] < q.y + h)
  // One L tile covers the centre square of each quadrant that does NOT contain Bill.
  out.push({ frame: { x, y, size: s }, cells: quads.filter((_, i) => i !== billQ).map((q) => q.centre), depth })
  quads.forEach((q, i) => solve(q.x, q.y, h, i === billQ ? b : q.centre, depth + 1, out))
}

const steps = computed(() => {
  const out: Step[] = []
  solve(0, 0, size.value, bill.value, 0, out)
  return out
})
const total = computed(() => steps.value.length)

watch(n, () => {
  const c = Math.floor(size.value / 2) - 1
  bill.value = [Math.max(c, 0), Math.max(c, 0)]
})
watch([n, bill], () => {
  stop()
  shown.value = 0
})

const VIEW = 400
const cell = computed(() => VIEW / size.value)
const palette = ['var(--viz-gold)', 'var(--viz-rose)', 'var(--viz-violet)', 'var(--viz-teal)', 'var(--viz-blue)']

function edges(cells: Cell[]) {
  const key = (c: number, r: number) => `${c},${r}`
  const set = new Set(cells.map(([c, r]) => key(c, r)))
  const s = cell.value
  const segs: string[] = []
  for (const [c, r] of cells) {
    const x = c * s
    const y = r * s
    if (!set.has(key(c, r - 1))) segs.push(`M${x},${y}h${s}`)
    if (!set.has(key(c, r + 1))) segs.push(`M${x},${y + s}h${s}`)
    if (!set.has(key(c - 1, r))) segs.push(`M${x},${y}v${s}`)
    if (!set.has(key(c + 1, r))) segs.push(`M${x + s},${y}v${s}`)
  }
  return segs.join('')
}

const current = computed(() => (shown.value > 0 ? steps.value[shown.value - 1] : null))

function next() {
  if (shown.value < total.value) shown.value++
  else stop()
}
function play() {
  if (shown.value >= total.value) shown.value = 0
  playing.value = true
  const delay = Math.max(40, 900 / total.value ** 0.6)
  timer = window.setInterval(() => {
    if (shown.value >= total.value) stop()
    else shown.value++
  }, delay)
}
function stop() {
  playing.value = false
  if (timer) clearInterval(timer)
  timer = undefined
}
onBeforeUnmount(stop)

function onClick(e: MouseEvent) {
  const svg = e.currentTarget as SVGSVGElement
  const r = svg.getBoundingClientRect()
  const c = Math.floor(((e.clientX - r.left) / r.width) * size.value)
  const row = Math.floor(((e.clientY - r.top) / r.height) * size.value)
  if (c >= 0 && c < size.value && row >= 0 && row < size.value) bill.value = [c, row]
}

const message = computed(() => {
  const s = current.value
  if (!s) return `Click any square to put Bill there. Then press Play or Step. You'll need (4^${n.value} − 1)/3 = ${total.value} tiles.`
  const h = s.frame.size / 2
  if (shown.value === total.value)
    return `Done: ${total.value} tiles, with Bill wherever you put him. The proof also told us how to build the tiling.`
  return `Depth ${s.depth}: split this ${s.frame.size}×${s.frame.size} block into four ${h}×${h} quadrants. One quadrant already has Bill (or a temporary Bill). Put one L tile on the centre squares of the other three. Now every quadrant is a smaller copy of the same problem.`
})
</script>

<template>
  <div class="viz">
    <div class="viz-title">Tiling Bill's courtyard: the proof is the algorithm</div>
    <div class="viz-hint">A 2ⁿ × 2ⁿ courtyard, one square taken by Bill's statue, every other square covered by L-shaped tiles. Click to move Bill, even to a corner.</div>
    <div class="stage">
      <svg :viewBox="`-2 -2 ${VIEW + 4} ${VIEW + 4}`" class="board" @click="onClick">
        <rect x="0" y="0" :width="VIEW" :height="VIEW" fill="var(--viz-bg)" />
        <g stroke="var(--viz-grid)" stroke-width="1">
          <line v-for="i in size - 1" :key="'v' + i" :x1="i * cell" :x2="i * cell" y1="0" :y2="VIEW" />
          <line v-for="i in size - 1" :key="'h' + i" :y1="i * cell" :y2="i * cell" x1="0" :x2="VIEW" />
        </g>
        <g v-for="(t, i) in steps.slice(0, shown)" :key="i" :class="{ fresh: i === shown - 1 }">
          <rect
            v-for="(c, j) in t.cells"
            :key="j"
            :x="c[0] * cell"
            :y="c[1] * cell"
            :width="cell"
            :height="cell"
            :fill="palette[t.depth % palette.length]"
            :opacity="i === shown - 1 ? 1 : [0.62, 0.78, 0.9][i % 3]"
          />
          <path :d="edges(t.cells)" stroke="var(--viz-panel)" stroke-width="2.5" fill="none" stroke-linecap="square" />
        </g>
        <g v-if="current && shown < total">
          <rect
            :x="current.frame.x * cell"
            :y="current.frame.y * cell"
            :width="current.frame.size * cell"
            :height="current.frame.size * cell"
            fill="none"
            stroke="var(--viz-ink)"
            stroke-width="2.5"
            stroke-dasharray="7 5"
          />
          <line
            :x1="(current.frame.x + current.frame.size / 2) * cell"
            :x2="(current.frame.x + current.frame.size / 2) * cell"
            :y1="current.frame.y * cell"
            :y2="(current.frame.y + current.frame.size) * cell"
            stroke="var(--viz-ink)"
            stroke-width="1.5"
            stroke-dasharray="3 4"
          />
          <line
            :y1="(current.frame.y + current.frame.size / 2) * cell"
            :y2="(current.frame.y + current.frame.size / 2) * cell"
            :x1="current.frame.x * cell"
            :x2="(current.frame.x + current.frame.size) * cell"
            stroke="var(--viz-ink)"
            stroke-width="1.5"
            stroke-dasharray="3 4"
          />
        </g>
        <g :transform="`translate(${(bill[0] + 0.5) * cell}, ${(bill[1] + 0.5) * cell})`">
          <circle :r="cell * 0.38" fill="var(--viz-ink)" />
          <text text-anchor="middle" dominant-baseline="central" :font-size="cell * 0.45" fill="var(--viz-panel)" font-weight="700">B</text>
        </g>
      </svg>
    </div>
    <div class="viz-controls">
      <label>n = {{ n }} ({{ size }}×{{ size }}) <input v-model.number="n" type="range" min="1" max="5" /></label>
      <button class="viz-btn primary" @click="playing ? stop() : play()">{{ playing ? 'Pause' : 'Play' }}</button>
      <button class="viz-btn" :disabled="playing || shown >= total" @click="next">Step</button>
      <button class="viz-btn" @click="stop(); shown = 0">Clear</button>
      <span class="count">{{ shown }} / {{ total }} tiles</span>
    </div>
    <div class="legend">
      Colour = recursion depth:
      <span v-for="d in Math.min(n, palette.length)" :key="d"><i :style="{ background: palette[(d - 1) % palette.length] }" />{{ d - 1 }}</span>
    </div>
    <div class="viz-readout">{{ message }}</div>
  </div>
</template>

<style scoped>
.stage { display: flex; justify-content: center; }
.board { max-width: 420px; cursor: crosshair; border-radius: 6px; }
.fresh rect { animation: pop 0.25s ease-out; transform-box: fill-box; transform-origin: center; }
@keyframes pop { from { transform: scale(0.6); opacity: 0; } }
.count { color: var(--viz-muted); font-family: var(--vp-font-family-mono); font-size: 0.85rem; }
.legend { font-size: 0.8rem; color: var(--viz-muted); display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 4px; vertical-align: -1px; }
</style>
