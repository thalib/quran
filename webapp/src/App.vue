<template>
  <div class="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <router-link class="navbar-brand" to="/">Quran Learning</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#nav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="nav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">
                <i class="bi bi-house"></i> Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/surahs">
                <i class="bi bi-book"></i> Surahs
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/history">
                <i class="bi bi-clock-history"></i> History
              </router-link>
            </li>
            <li class="nav-item">
              <button
                class="nav-link btn btn-link"
                type="button"
                data-bs-toggle="offcanvas"
                data-bs-target="#settingsOffcanvas"
              >
                <i class="bi bi-gear"></i> Settings
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <main class="container mt-4">
      <router-view />
    </main>
    <div
      class="offcanvas offcanvas-end"
      tabindex="-1"
      id="settingsOffcanvas"
      data-bs-scroll="true"
      aria-labelledby="settingsOffcanvasLabel"
    >
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="settingsOffcanvasLabel">Settings</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="offcanvas"
          aria-label="Close"
        ></button>
      </div>
      <div class="offcanvas-body">
        <h6 class="mb-3 mt-2 border-bottom pb-2 text-muted small uppercase">
          Font Size
        </h6>
        <div class="mb-3">
          <label for="arabicFontSize" class="form-label"
            >Arabic font size</label
          >
          <input
            id="arabicFontSize"
            type="range"
            class="form-range"
            min="12"
            max="48"
            step="2"
            :value="arabicFontSizePx"
            @input="updateArabic"
          />
          <span class="ms-2">{{ arabicFontSizePx }} px</span>
        </div>
        <div class="mb-3">
          <label for="englishFontSize" class="form-label"
            >English font size</label
          >
          <input
            id="englishFontSize"
            type="range"
            class="form-range"
            min="12"
            max="48"
            step="2"
            :value="englishFontSizePx"
            @input="updateEnglish"
          />
          <span class="ms-2">{{ englishFontSizePx }} px</span>
        </div>
        <h6 class="mb-3 mt-4 border-bottom pb-2 text-muted small uppercase">
          Display
        </h6>
        <div class="mb-3 form-check">
          <input
            class="form-check-input"
            type="checkbox"
            id="showArabicVerse"
            v-model="showArabicVerse"
            @change="apply"
          />
          <label class="form-check-label" for="showArabicVerse"
            >Show Arabic verse</label
          >
        </div>
        <div class="mb-3 form-check">
          <input
            class="form-check-input"
            type="checkbox"
            id="showWordMeanings"
            v-model="showWordMeanings"
            @change="apply"
          />
          <label class="form-check-label" for="showWordMeanings"
            >Show word-by-word meanings</label
          >
        </div>
        <div class="mb-3 form-check">
          <input
            class="form-check-input"
            type="checkbox"
            id="showTranslation"
            v-model="showTranslation"
            @change="apply"
          />
          <label class="form-check-label" for="showTranslation"
            >Show verse translation</label
          >
        </div>
        <h6 class="mb-3 mt-4 border-bottom pb-2 text-muted small uppercase">
          Preferences
        </h6>
        <div class="mb-3">
          <label for="theme" class="form-label">Theme</label>
          <select
            id="theme"
            class="form-select form-select-sm"
            v-model="theme"
            @change="apply"
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </div>
        <div class="mb-3 form-check">
          <input
            class="form-check-input"
            type="checkbox"
            id="autoSave"
            v-model="autoSave"
            @change="apply"
          />
          <label class="form-check-label" for="autoSave">Auto-save answers</label>
        </div>
        <div class="mb-3">
          <label for="interfaceLanguage" class="form-label"
            >Interface language</label
          >
          <select
            id="interfaceLanguage"
            class="form-select form-select-sm"
            v-model="interfaceLanguage"
            @change="apply"
          >
            <option value="en">English</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="meaningLanguage" class="form-label"
            >Meaning language</label
          >
          <select
            id="meaningLanguage"
            class="form-select form-select-sm"
            v-model="meaningLanguage"
            @change="apply"
          >
            <option value="en">English</option>
          </select>
        </div>
        <div class="mb-3">
          <button
            type="button"
            class="btn btn-outline-danger btn-sm"
            @click="resetProgress"
          >
            Clear progress
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSettings } from "./composables/useSettings.js";
import { clearProgress } from "./services/progressService.js";
import { computed } from "vue";

const REM_BASE = 16;

const {
  arabicFontSize,
  englishFontSize,
  showArabicVerse,
  showWordMeanings,
  showTranslation,
  theme,
  autoSave,
  interfaceLanguage,
  meaningLanguage,
  apply,
} = useSettings();

function resetProgress() {
  if (window.confirm("Clear all progress?")) {
    clearProgress();
  }
}

const arabicFontSizePx = computed({
  get() {
    return Math.round(parseFloat(arabicFontSize.value) * REM_BASE);
  },
  set(val) {
    arabicFontSize.value = `${val / REM_BASE}rem`;
    apply();
  },
});

const englishFontSizePx = computed({
  get() {
    return Math.round(parseFloat(englishFontSize.value) * REM_BASE);
  },
  set(val) {
    englishFontSize.value = `${val / REM_BASE}rem`;
    apply();
  },
});

function updateArabic(event) {
  arabicFontSizePx.value = Number(event.target.value);
}

function updateEnglish(event) {
  englishFontSizePx.value = Number(event.target.value);
}
</script>
