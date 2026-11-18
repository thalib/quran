<template>
  <div>
    <h1 class="mb-3">History</h1>
    <p v-if="history.length === 0" class="text-muted">No history yet.</p>
    <div class="card mb-3" v-for="h in history" :key="h.surahId">
      <div class="card-body">
        <h5>Surah {{ h.surahId }}</h5>
        <ul class="list-unstyled mb-2">
          <li>Attempts: {{ h.totalAttempts ?? h.attempts }}</li>
          <li>Latest score: {{ h.latestScore }}%</li>
          <li>Best score: {{ h.bestScore }}%</li>
          <li>Last practiced: {{ formatDate(h.lastVisitedDate ?? h.lastPracticed) }}</li>
        </ul>
        <router-link
          :to="`/surah/${h.surahId}/results`"
          class="btn btn-sm btn-outline-primary"
        >
          View results
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { getHistory } from "../services/progressService.js";

const history = ref([]);

function formatDate(value) {
  if (!value) return "—";
  try {
    return new Date(value).toLocaleString();
  } catch {
    return value;
  }
}

onMounted(() => {
  history.value = getHistory();
});
</script>
