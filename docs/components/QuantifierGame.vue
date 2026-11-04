<script setup lang="ts">
// The ∀/∃ game: the opponent picks for ∀, you pick for ∃, in order.
// A statement is true exactly when you have a winning strategy.
// Truth values and the opponent's moves are computed by quantifiers.ts.
import { computed, ref } from 'vue'
import { DOMAIN, STATEMENTS, opponentPick, truth, winningPick } from './quantifiers'

const idx = ref(0)
const s = computed(() => STATEMENTS[idx.value])
const prediction = ref<boolean | null>(null)
const picks = ref<Record<string, number>>({})
const depth = ref(0)
const hint = ref<string | null>(null)

const isTrue = computed(() => truth(s.value))
const finished = computed(() => depth.value === s.value.quants.length)
const won = computed(() => finished.value && s.value.pred(picks.value))
const yourTurn = computed(() => !finished.value && s.value.quants[depth.value][0] === 'E')

function advance() {
  // Let the opponent play every ∀ that comes up until it's your turn or the game ends.
  while (depth.value < s.value.quants.length && s.value.quants[depth.value][0] === 'A') {
    const [, v] = s.value.quants[depth.value]
    picks.value = { ...picks.value, [v]: opponentPick(s.value, picks.value, depth.value) }
    depth.value++
  }
}
function predict(p: boolean) {
  prediction.value = p
  advance()
}
function choose(d: number) {
  const before = { ...picks.value }
  const at = depth.value
  const [, v] = s.value.quants[at]
  picks.value = { ...picks.value, [v]: d }
  depth.value++
  const best = winningPick(s.value, before, at)
  hint.value = best !== null && !truth(s.value, picks.value, at + 1) ? `${v} = ${best} would have won from there.` : null
  advance()
}
function reset(i = idx.value) {
  idx.value = i
  prediction.value = null
  picks.value = {}
  depth.value = 0
  hint.value = null
}
function replay() {
  const keep = prediction.value
  reset()
  prediction.value = keep
  advance()
}
</script>

<template>
  <div class="viz" data-viz="QuantifierGame">
    <div class="viz-title">The quantifier game</div>
    <div class="viz-hint">Domain D = {{ '{' + DOMAIN.join(', ') + '}' }}. Read left to right. For ∀ your opponent picks; for ∃ you pick. You win if the last part is true.</div>
    <div class="tabs">
      <button v-for="(t, i) in STATEMENTS" :key="t.id" class="viz-btn" :class="{ primary: i === idx }" @click="reset(i)">{{ i + 1 }}</button>
    </div>
    <p class="stmt">{{ s.text }}</p>

    <div v-if="prediction === null" class="viz-controls">
      <span>First predict: is it true over D?</span>
      <button class="viz-btn" @click="predict(true)">True</button>
      <button class="viz-btn" @click="predict(false)">False</button>
    </div>

    <template v-else>
      <ol class="moves">
        <li v-for="(q, i) in s.quants.slice(0, depth)" :key="i">
          {{ q[0] === 'A' ? 'Opponent (∀) picks' : 'You (∃) picked' }} {{ q[1] }} = <b>{{ picks[q[1]] }}</b>
        </li>
      </ol>
      <div v-if="yourTurn" class="viz-controls">
        <span>Your move: pick {{ s.quants[depth][1] }}</span>
        <button v-for="d in DOMAIN" :key="d" class="viz-btn" @click="choose(d)">{{ d }}</button>
      </div>
      <div v-if="finished" class="viz-readout">
        <p><b>{{ won ? 'You win this round.' : 'You lose this round.' }}</b> <span v-if="hint">{{ hint }}</span></p>
        <p>
          The statement is <b>{{ isTrue ? 'true' : 'false' }}</b> over D. You predicted {{ prediction ? 'true' : 'false' }}{{ prediction === isTrue ? ' ✓' : ' ✗' }}.
          <template v-if="isTrue && !won"> A true statement means you <i>can</i> always win, so try again.</template>
          <template v-if="!isTrue"> A false statement means the opponent can always beat you, whatever you pick.</template>
        </p>
        <p>{{ s.lesson }}</p>
        <div class="viz-controls">
          <button class="viz-btn" @click="replay">Play again</button>
          <button v-if="idx < STATEMENTS.length - 1" class="viz-btn primary" @click="reset(idx + 1)">Next statement</button>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.tabs { display: flex; gap: 6px; flex-wrap: wrap; margin: 8px 0; }
.stmt { font-size: 1.25rem; font-weight: 600; text-align: center; margin: 12px 0; }
.moves { margin: 6px 0; padding-left: 1.4em; }
.viz-readout p { margin: 6px 0; }
</style>
