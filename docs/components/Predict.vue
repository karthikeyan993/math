<script setup lang="ts">
import { ref } from 'vue'
defineProps<{ question: string }>()
const guess = ref('')
const revealed = ref(false)
const confidence = ref<string | null>(null)
function lock(c: string) {
  confidence.value = c
  revealed.value = true
}
</script>

<template>
  <div class="predict">
    <div class="tag">Predict first</div>
    <p class="q">{{ question }}</p>
    <template v-if="!revealed">
      <textarea v-model="guess" rows="2" placeholder="Write your guess. Being wrong here is the point: it makes the answer stick." />
      <div class="conf">
        <span>How sure are you?</span>
        <button class="viz-btn" @click="lock('guessing')">Guessing</button>
        <button class="viz-btn" @click="lock('fairly sure')">Fairly sure</button>
        <button class="viz-btn" @click="lock('certain')">Certain</button>
      </div>
    </template>
    <div v-else class="answer">
      <p class="yours"><span>You said ({{ confidence }}):</span> {{ guess.trim() || '(nothing written)' }}</p>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.predict {
  border-left: 4px solid var(--viz-gold);
  background: color-mix(in srgb, var(--viz-gold) 8%, transparent);
  border-radius: 0 10px 10px 0;
  padding: 12px 16px;
  margin: 20px 0;
}
.tag { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--viz-gold); font-weight: 700; }
.q { margin: 6px 0 10px; font-weight: 500; }
textarea {
  width: 100%;
  background: var(--viz-panel);
  color: var(--viz-ink);
  border: 1px solid var(--viz-grid);
  border-radius: 8px;
  padding: 8px;
  font: inherit;
  font-size: 0.9rem;
  margin-bottom: 8px;
  resize: vertical;
}
.conf { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; font-size: 0.85rem; color: var(--viz-muted); }
.yours { color: var(--viz-muted); font-style: italic; }
.yours span { font-style: normal; font-weight: 600; }
.answer :deep(p:first-child) { margin-top: 0; }
</style>
