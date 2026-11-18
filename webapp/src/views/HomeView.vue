<template>
  <div>
    <h1 class="mb-3">Quran Learning</h1>
    <p class="lead">Learn the Quran, one word at a time.</p>
    <router-link to="/surahs" class="btn btn-primary mb-4">
      Browse Surahs
    </router-link>

    <div v-if="history.length" class="card">
      <div class="card-body">
        <h5 class="card-title">Progress</h5>
        <ul class="list-unstyled mb-0">
          <li v-for="h in history" :key="h.surahId">
            Surah {{ h.surahId }} — attempts: {{ h.totalAttempts ?? h.attempts }},
            best: {{ h.bestScore }}%
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { getHistory } from "../services/progressService.js";

const history = ref([]);

onMounted(() => {
  history.value = getHistory();
});
</script>
