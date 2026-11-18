<template>
  <div>
    <h1 class="mb-3">Learning</h1>
    <p v-if="loading">Loading...</p>
    <p v-else-if="error" class="text-danger">Failed to load surah.</p>
    <template v-else-if="surah">
      <div class="mb-3">
        <h2>{{ surah.surah.name.english }} ({{ surah.surah.name.arabic }})</h2>
        <p class="text-muted">{{ surah.surah.name.transliteration }}</p>
      </div>
      <div v-for="(verse, vIndex) in surah.verses" :key="verse.id" class="card mb-3">
        <div class="card-body">
          <h5>Verse {{ verse.number }}</h5>
          <div
            v-if="showArabicVerse"
            class="arabic-text mb-2"
            dir="rtl"
          >
            {{ verse.arabic.text }}
          </div>
          <div
            v-if="showWordMeanings"
            class="d-flex flex-wrap gap-3 mb-2"
            dir="rtl"
          >
            <div
              v-for="(word, wIndex) in verse.words"
              :key="word.id"
              :class="[
                'text-center',
                'word-clickable',
                'word-color-' + ((vIndex * 7 + wIndex) % 5),
              ]"
              role="button"
              tabindex="0"
              @click="openWord(word)"
              @keydown.enter="openWord(word)"
              @keydown.space.prevent="openWord(word)"
            >
              <div class="arabic-text">{{ word.arabic }}</div>
              <div class="small text-muted english-text">
                {{ word.meanings.en.primary }}
              </div>
            </div>
          </div>
          <p
            v-if="
              showTranslation &&
              verse.translation &&
              verse.translation.en
            "
            class="english-text"
          >
            <strong>Translation:</strong> {{ verse.translation.en.text }}
          </p>
          <p v-if="verse.explanation" class="english-text">
            <strong>Explanation:</strong> {{ verse.explanation }}
          </p>
        </div>
      </div>
    </template>
  </div>
  <div v-if="selectedWord" class="word-details" role="dialog" aria-label="Word details">
    <div class="word-details-backdrop" @click="closeWord"></div>
    <div class="word-details-panel">
      <button
        type="button"
        class="btn-close float-end"
        aria-label="Close"
        @click="closeWord"
      ></button>
      <h5 class="arabic-text mb-1">{{ selectedWord.arabic }}</h5>
      <p class="text-muted mb-3">{{ selectedWord.transliteration }}</p>
      <dl class="mb-0">
        <dt>Meaning</dt>
        <dd class="english-text">{{ selectedWord.meanings?.en?.primary }}</dd>
        <template v-if="selectedWord.meanings?.en?.alternatives?.length">
          <dt>Alternatives</dt>
          <dd class="english-text">
            {{ selectedWord.meanings.en.alternatives.join(", ") }}
          </dd>
        </template>
        <template v-if="selectedWord.root">
          <dt>Root</dt>
          <dd>
            {{
              typeof selectedWord.root === "string"
                ? selectedWord.root
                : selectedWord.root.text || selectedWord.root.arabic || ""
            }}
          </dd>
          <template
            v-if="
              typeof selectedWord.root === 'object' && selectedWord.root.meaning
            "
          >
            <dt>Root meaning</dt>
            <dd class="english-text">{{ selectedWord.root.meaning }}</dd>
          </template>
        </template>
        <template v-if="selectedWord.grammar">
          <dt>Grammar</dt>
          <dd>
            {{
              typeof selectedWord.grammar === "string"
                ? selectedWord.grammar
                : JSON.stringify(selectedWord.grammar)
            }}
          </dd>
        </template>
        <template v-if="selectedWord.explanation">
          <dt>Explanation</dt>
          <dd class="english-text">{{ selectedWord.explanation }}</dd>
        </template>
      </dl>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useQuran } from "../composables/useQuran.js";
import { useSettings } from "../composables/useSettings.js";

const route = useRoute();
const { surah, loading, error, load } = useQuran();
const {
  showArabicVerse,
  showWordMeanings,
  showTranslation,
} = useSettings();

const selectedWord = ref(null);
function openWord(word) {
  selectedWord.value = word;
}
function closeWord() {
  selectedWord.value = null;
}

onMounted(() => {
  load(route.params.id);
});
</script>

<style scoped>
.word-clickable {
  cursor: pointer;
  padding: 0.35rem 0.5rem;
  border-radius: 0.375rem;
  transition: background-color 0.15s ease;
}

.word-clickable:hover,
.word-clickable:focus {
  background-color: var(--bs-secondary-bg, rgba(0, 0, 0, 0.05));
}

.word-clickable:hover .arabic-text,
.word-clickable:focus .arabic-text {
  text-decoration: none;
}

.word-color-0 .arabic-text { color: #1f6feb; }
.word-color-1 .arabic-text { color: #cf6a00; }
.word-color-2 .arabic-text { color: #1a7f37; }
.word-color-3 .arabic-text { color: #cf222e; }
.word-color-4 .arabic-text { color: #8250df; }

.word-details-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1040;
}

.word-details-panel {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-height: 70vh;
  overflow-y: auto;
  background: var(--bs-body-bg, #fff);
  z-index: 1050;
  padding: 1rem;
  border-top: 1px solid var(--bs-border-color, #dee2e6);
}

@media (min-width: 768px) {
  .word-details-panel {
    top: 0;
    right: 0;
    bottom: 0;
    left: auto;
    width: 360px;
    max-height: none;
    border-left: 1px solid var(--bs-border-color, #dee2e6);
    border-top: none;
  }
}
</style>
