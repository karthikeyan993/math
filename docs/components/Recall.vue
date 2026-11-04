<script setup lang="ts">
import { ref } from 'vue'
defineProps<{ q: string }>()
const shown = ref(false)
const rating = ref<string | null>(null)
const notes: Record<string, string> = {
  got: 'Nice. You will see it again in the flashcards in a few days.',
  shaky: 'Normal on a first pass. Re-read the section above once, then try again tomorrow.',
  missed: 'Good to know now rather than in a pset. Re-do the interactive above, then retry.',
}
</script>

<template>
  <div class="recall">
    <p class="q">{{ q }}</p>
    <button v-if="!shown" class="viz-btn" @click="shown = true">Answer it in your head, then reveal</button>
    <div v-else>
      <div class="a"><slot /></div>
      <div class="rate">
        <span>How did you do?</span>
        <button class="viz-btn" :class="{ primary: rating === 'got' }" @click="rating = 'got'">Got it</button>
        <button class="viz-btn" :class="{ primary: rating === 'shaky' }" @click="rating = 'shaky'">Shaky</button>
        <button class="viz-btn" :class="{ primary: rating === 'missed' }" @click="rating = 'missed'">Missed</button>
      </div>
      <p v-if="rating" class="note">{{ notes[rating] }}</p>
    </div>
  </div>
</template>

<style scoped>
.recall { border: 1px solid var(--viz-grid); border-radius: 10px; padding: 12px 16px; margin: 14px 0; background: var(--viz-panel); }
.q { margin: 0 0 10px; font-weight: 500; }
.a { border-top: 1px dashed var(--viz-grid); padding-top: 8px; }
.a :deep(p) { margin: 6px 0; }
.rate { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-top: 10px; font-size: 0.85rem; color: var(--viz-muted); }
.note { font-size: 0.85rem; color: var(--viz-muted); margin: 8px 0 0; }
</style>
