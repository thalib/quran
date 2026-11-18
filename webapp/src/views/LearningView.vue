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
      <div class="mb-3 d-flex flex-wrap gap-2 align-items-center">
        <div class="btn-group" role="group" aria-label="Learning mode">
          <button
            type="button"
            class="btn btn-sm"
            :class="mode === 'reading' ? 'btn-primary' : 'btn-outline-primary'"
            @click="mode = 'reading'"
          >
            Reading
          </button>
          <button
            type="button"
            class="btn btn-sm"
            :class="mode === 'test' ? 'btn-primary' : 'btn-outline-primary'"
            @click="mode = 'test'"
          >
            Test
          </button>
        </div>
        <div v-if="mode === 'test'" class="d-flex flex-wrap gap-2 align-items-center">
          <label for="scope" class="form-label mb-0 small">Scope</label>
          <select id="scope" v-model="scope" class="form-select form-select-sm" style="width: auto">
            <option value="surah">Entire Surah</option>
            <option value="verse">Individual Verse</option>
          </select>
          <select
            v-if="scope === 'verse'"
            v-model="selectedVerseNumber"
            class="form-select form-select-sm"
            style="width: auto"
            aria-label="Select verse"
          >
            <option v-for="v in surah.verses" :key="v.id" :value="v.number">
              Verse {{ v.number }}
            </option>
          </select>
        </div>
      </div>
      <div v-for="(verse, vIndex) in visibleVerses" :key="verse.id" class="card mb-3">
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
                mode === 'reading' ? 'word-clickable' : '',
                'word-color-' + ((vIndex * 7 + wIndex) % 5),
              ]"
              :role="mode === 'reading' ? 'button' : undefined"
              :tabindex="mode === 'reading' ? 0 : -1"
              @click="mode === 'reading' && openWord(word)"
              @keydown.enter="mode === 'reading' && openWord(word)"
              @keydown.space.prevent="mode === 'reading' && openWord(word)"
            >
              <div class="arabic-text">{{ word.arabic }}</div>
              <input
                v-if="mode === 'test'"
                v-model="answers[word.id]"
                type="text"
                dir="ltr"
                lang="en"
                autocomplete="off"
                spellcheck="false"
                class="form-control form-control-sm mt-1 test-input"
                @input="saveAnswers"
              />
              <div
                v-else-if="showWordMeanings"
                class="small text-muted english-text"
              >
                {{ word.meanings.en.primary }}
              </div>
            </div>
            </div>
           <p
            v-if="
              mode === 'reading' &&
              showTranslation &&
              verse.translation &&
              verse.translation.en
            "
            class="english-text"
          >
            <strong>Translation:</strong> {{ verse.translation.en.text }}
          </p>
          <p
            v-if="mode === 'reading' && verse.explanation"
            class="english-text"
          >
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
import { onMounted, ref, computed, watch } from "vue";
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

const mode = ref("reading");
const scope = ref("surah");
const selectedVerseNumber = ref(1);
const selectedWord = ref(null);
const answers = ref({});

watch(
  answers,
  () => {
    saveAnswers();
  },
  { deep: true },
);
const visibleVerses = computed(() => {
  if (!surah.value) return [];
  if (mode.value !== "test" || scope.value === "surah") {
    return surah.value.verses;
  }
  return surah.value.verses.filter(
    (v) => v.number === selectedVerseNumber.value,
  );
});

function storageKey() {
  return surah.value ? `quran:answers:surah:${surah.value.surah.id}` : null;
}

function loadAnswers() {
  answers.value = {};
  const key = storageKey();
  if (!key) return;
  try {
    const raw = localStorage.getItem(key);
    if (raw) answers.value = JSON.parse(raw);
  } catch {
    answers.value = {};
  }
}

function saveAnswers() {
  const key = storageKey();
  if (!key) return;
  try {
    localStorage.setItem(key, JSON.stringify(answers.value));
  } catch {
    // ignore
  }
}

function openWord(word) {
  selectedWord.value = word;
}
function closeWord() {
  selectedWord.value = null;
}

watch(
  () => route.params.id,
  async (id) => {
    if (id) {
      await load(id);
      loadAnswers();
    }
  },
);

onMounted(async () => {
  await load(route.params.id);
  loadAnswers();
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
.test-input {
  border-radius: 2rem;
  padding: 0.5rem 1rem;
  text-align: center;
}
</style>
