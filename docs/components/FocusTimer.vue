<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const KEY = 'mcs-focus-minutes'
const options = [10, 15, 20, 25, 30, 40, 50]
const minutes = ref(15)
const goal = ref('')
const state = ref<'idle' | 'running' | 'reentry' | 'done'>('idle')
const remaining = ref(0)
const drifts = ref(0)
const open = ref(false)
let timer: number | undefined

onMounted(() => {
  try {
    const v = Number(localStorage.getItem(KEY))
    if (options.includes(v)) minutes.value = v
  } catch {}
})
onBeforeUnmount(() => clearInterval(timer))

function start() {
  try { localStorage.setItem(KEY, String(minutes.value)) } catch {}
  remaining.value = minutes.value * 60
  drifts.value = 0
  state.value = 'running'
  clearInterval(timer)
  timer = window.setInterval(() => {
    if (state.value !== 'running') return
    remaining.value--
    if (remaining.value <= 0) {
      clearInterval(timer)
      state.value = 'done'
      open.value = true
    }
  }, 1000)
}
function drifted() {
  drifts.value++
  state.value = 'reentry'
  open.value = true
}
function resume() {
  state.value = 'running'
}
function reset() {
  clearInterval(timer)
  state.value = 'idle'
}
const clock = computed(() => {
  const m = Math.floor(remaining.value / 60)
  const s = remaining.value % 60
  return `${m}:${String(s).padStart(2, '0')}`
})
const next = computed(() => options.find((o) => o > minutes.value) ?? minutes.value)
const logLine = computed(
  () => `Focus block: ${minutes.value} min, drifted ${drifts.value}×. Goal: ${goal.value || '(none set)'}`,
)
</script>

<template>
  <div class="focus" :class="{ open }">
    <button class="pill" @click="open = !open" :aria-expanded="open">
      <span v-if="state === 'running'">● {{ clock }}</span>
      <span v-else-if="state === 'reentry'">↺ re-entry</span>
      <span v-else-if="state === 'done'">✓ block done</span>
      <span v-else>Focus block</span>
    </button>
    <div v-if="open" class="panel">
      <template v-if="state === 'idle'">
        <p class="h">One goal, one time box</p>
        <input v-model="goal" placeholder="This block I will… (e.g. finish §3 and its recall Qs)" />
        <div class="row">
          <label>Length
            <select v-model.number="minutes">
              <option v-for="o in options" :key="o" :value="o">{{ o }} min</option>
            </select>
          </label>
          <button class="viz-btn primary" @click="start">Start</button>
        </div>
        <p class="tip">Choose a length you can <i>finish</i> without drifting. Go one step longer only after a few clean blocks.</p>
      </template>
      <template v-else-if="state === 'running'">
        <p class="h">{{ clock }} left</p>
        <p class="tip" v-if="goal">Goal: {{ goal }}</p>
        <div class="row">
          <button class="viz-btn" @click="drifted">I drifted</button>
          <button class="viz-btn" @click="reset">Stop</button>
        </div>
        <p class="tip">Unrelated thought? Jot it on paper and come back. Don't act on it now.</p>
      </template>
      <template v-else-if="state === 'reentry'">
        <p class="h">Re-entry, 30 seconds</p>
        <ol class="tip">
          <li>Re-read the last heading you were on.</li>
          <li>Say out loud what you were trying to figure out.</li>
          <li>Do the very next small action: one line, one click, one guess.</li>
        </ol>
        <button class="viz-btn primary" @click="resume">Back in</button>
      </template>
      <template v-else>
        <p class="h">Block done. Stop at the next sentence.</p>
        <p class="tip">Write one line on where you are and what's next, then take a real break away from the screen.</p>
        <code class="log">{{ logLine }}</code>
        <p class="tip" v-if="drifts === 0 && next !== minutes">A clean block. If the last 3 were clean too, try {{ next }} min next time.</p>
        <button class="viz-btn" @click="reset">New block</button>
      </template>
    </div>
  </div>
</template>

<style scoped>
.focus { position: fixed; right: 16px; bottom: 16px; z-index: 30; font-size: 0.85rem; }
.pill {
  background: var(--viz-panel); color: var(--viz-ink); border: 1px solid var(--viz-grid);
  border-radius: 999px; padding: 6px 14px; cursor: pointer; box-shadow: 0 4px 16px rgb(0 0 0 / 0.25);
  font-family: var(--vp-font-family-mono);
}
.panel {
  position: absolute; right: 0; bottom: 44px; width: min(320px, calc(100vw - 32px));
  background: var(--viz-panel); border: 1px solid var(--viz-grid); border-radius: 12px; padding: 12px 14px;
  box-shadow: 0 8px 28px rgb(0 0 0 / 0.3);
}
.h { font-weight: 600; margin: 0 0 8px; color: var(--viz-ink); }
.tip { color: var(--viz-muted); margin: 8px 0 0; line-height: 1.45; }
ol.tip { padding-left: 18px; margin-bottom: 10px; }
.row { display: flex; gap: 8px; align-items: center; justify-content: space-between; margin-top: 8px; }
input, select {
  width: 100%; background: var(--viz-bg); color: var(--viz-ink); border: 1px solid var(--viz-grid);
  border-radius: 6px; padding: 5px 8px; font: inherit;
}
select { width: auto; margin-left: 6px; }
.log { display: block; margin: 8px 0; font-size: 0.78rem; white-space: normal; }
</style>
