<script setup lang="ts">
// Which cards could falsify "if P then Q"? (Wason's selection task.)
// `answer` lists the card indices that must be turned; tools/verify/components.py
// re-derives it by brute force and checks it against every use in a lesson.
import { computed, ref } from 'vue'

const props = defineProps<{ rule: string; cards: string; answer: string }>()
const faces = computed(() => props.cards.split(',').map((s) => s.trim()))
const must = computed(() => new Set(props.answer.split(',').map(Number)))
const picked = ref<Set<number>>(new Set())
const done = ref(false)

function toggle(i: number) {
  if (done.value) return
  const s = new Set(picked.value)
  s.has(i) ? s.delete(i) : s.add(i)
  picked.value = s
}
const right = computed(() => faces.value.every((_, i) => picked.value.has(i) === must.value.has(i)))
</script>

<template>
  <div class="viz" data-viz="WasonCards">
    <div class="viz-title">Which cards must you turn over?</div>
    <p class="rule">Each card has a letter on one side and a number on the other. Rule: <b>{{ rule }}</b></p>
    <div class="viz-hint">Pick exactly the cards you must turn over to find out whether the rule is broken. No more, no fewer.</div>
    <div class="cards">
      <button v-for="(f, i) in faces" :key="i" class="card" :class="{ sel: picked.has(i), must: done && must.has(i) }" @click="toggle(i)">{{ f }}</button>
    </div>
    <div class="viz-controls">
      <button class="viz-btn primary" :disabled="done" @click="done = true">Check my picks</button>
      <button v-if="done" class="viz-btn" @click="done = false; picked = new Set()">Try again</button>
    </div>
    <div v-if="done" class="viz-readout">
      <p><b>{{ right ? 'Correct.' : 'Not quite.' }}</b> The cards that must be turned are outlined: {{ [...must].map((i) => faces[i]).join(' and ') }}.</p>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.rule { margin: 6px 0; }
.cards { display: flex; gap: 12px; justify-content: center; margin: 14px 0; flex-wrap: wrap; }
.card { width: 64px; height: 88px; border-radius: 10px; border: 2px solid var(--viz-grid); background: var(--viz-panel); color: var(--viz-ink); font-size: 1.6rem; font-weight: 700; cursor: pointer; }
.card.sel { border-color: var(--viz-blue); background: color-mix(in srgb, var(--viz-blue) 14%, transparent); }
.card.must { outline: 3px solid var(--viz-gold); outline-offset: 3px; }
.viz-readout :deep(p) { margin: 6px 0; }
</style>
