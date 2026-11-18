<template>
  <div>
    <h1 class="mb-3">Results</h1>
    <p v-if="loading">Loading...</p>
    <p v-else-if="error" class="text-danger">{{ error }}</p>
    <template v-else-if="data">
      <div class="card mb-3">
        <div class="card-body">
          <h5>Summary</h5>
          <ul class="list-unstyled mb-0">
            <li>Total words: {{ summary.totalWords ?? summary.total }}</li>
            <li>
              Attempted: {{ summary.attemptedAnswers ?? summary.attempted }}
            </li>
            <li>Correct: {{ summary.correctAnswers ?? summary.correct }}</li>
            <li>
              Incorrect: {{ summary.incorrectAnswers ?? summary.incorrect }}
            </li>
            <li>
              Unanswered: {{ summary.unansweredWords ?? summary.unanswered }}
            </li>
            <li>
              Overall score:
              {{ summary.overallScore ?? summary.overall ?? summary.score }}%
            </li>
            <li>
              Attempted accuracy:
              {{ summary.attemptedAccuracy ?? summary.attempted_accuracy }}%
            </li>
          </ul>
        </div>
      </div>

      <div class="card mb-3" v-if="verseScores && verseScores.length">
        <div class="card-body">
          <h5>Verse-level scores</h5>
          <ul class="list-group list-group-flush">
            <li
              class="list-group-item d-flex justify-content-between"
              v-for="vs in verseScores"
              :key="vs.verseNumber ?? vs.verse"
            >
              <span>Verse {{ vs.verseNumber ?? vs.verse }}</span>
              <span>
                {{ vs.correctAnswers ?? vs.correct }}/{{
                  vs.totalWords ?? vs.total
                }}
                ({{ vs.overallScore ?? vs.overall ?? vs.score }}%)
              </span>
            </li>
          </ul>
        </div>
      </div>

      <div class="card mb-3">
        <div class="card-body">
          <h5>Word-level corrections</h5>
          <div
            class="mb-2 pb-2 border-bottom"
            v-for="(r, i) in results"
            :key="i"
          >
            <div class="arabic-text" dir="rtl">{{ r.arabic }}</div>
            <div class="small">
              Your answer: {{ r.userAnswer || "(empty)" }}
            </div>
            <div class="small text-muted" v-if="r.status !== 'correct'">
              Suggested: {{ r.primary || r.primaryMeaning }}
            </div>
            <div
              class="small text-muted"
              v-if="
                r.status !== 'correct' &&
                (r.acceptedAnswers || r.accepted_answers || []).length
              "
            >
              Accepted:
              {{ (r.acceptedAnswers || r.accepted_answers || []).join(", ") }}
            </div>
            <div class="small">
              Status:
              <span
                :class="
                  r.status === 'correct'
                    ? 'text-success'
                    : r.status === 'unanswered'
                      ? 'text-warning'
                      : 'text-danger'
                "
              >
                {{ r.status }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <router-link
        :to="`/surah/${route.params.id}`"
        class="btn btn-outline-primary"
      >
        Return to Reading
      </router-link>
    </template>
    <template v-else>
      <p>No results found.</p>
      <router-link
        :to="`/surah/${route.params.id}`"
        class="btn btn-outline-primary"
      >
        Return to Reading
      </router-link>
    </template>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const loading = ref(false);
const error = ref("");
const data = ref(null);

const summary = computed(() => (data.value ? data.value.summary : null));
const verseScores = computed(() =>
  data.value ? data.value.verseScores || [] : [],
);
const results = computed(() => (data.value ? data.value.results || [] : []));

onMounted(() => {
  try {
    const raw = localStorage.getItem(`quran:results:surah:${route.params.id}`);
    if (raw) data.value = JSON.parse(raw);
  } catch (e) {
    error.value = "Failed to load results.";
  }
});
</script>
