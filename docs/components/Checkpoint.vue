<script setup lang="ts">
defineProps<{ n: number; of: number; next?: string }>()
</script>

<template>
  <div class="cp">
    <div class="bar"><span v-for="i in of" :key="i" :class="{ on: i <= n }" /></div>
    <div class="txt">
      <b>Checkpoint {{ n }} of {{ of }}.</b>
      <template v-if="n < of"> A good place to stop. <span v-if="next">Next sitting: {{ next }}</span></template>
      <template v-else> Lesson done. Log it, then do the textbook problems in a separate sitting.</template>
    </div>
  </div>
</template>

<style scoped>
.cp { margin: 36px 0; padding: 12px 16px; border-radius: 10px; background: color-mix(in srgb, var(--viz-teal) 10%, transparent); border: 1px dashed var(--viz-teal); }
.bar { display: flex; gap: 6px; margin-bottom: 8px; }
.bar span { flex: 1; height: 6px; border-radius: 3px; background: var(--viz-grid); }
.bar span.on { background: var(--viz-teal); }
.txt { font-size: 0.9rem; color: var(--viz-ink); }
</style>
