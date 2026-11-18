# Quran Learning App

**Document Version:** 1.1  
**Status:** Phase 1 — Foundation (in progress)  
**Last updated:** 2026-11-18  
**Code reflects:** `webapp/src/` as committed

---

## 1. Purpose

Lightweight, offline-first Quran learning SPA. Users read Quranic Arabic word by word with English meanings, translations, and self-assessment.

**Guiding principle:** Learn the Quran, one word at a time. Prioritize content accuracy, simple UX, mobile-first design, speed, offline capability, and maintainability.

---

## 2. Technology Stack (implemented)

| Category | Technology |
|---|---|
| Framework | Vue 3 (Composition API, `<script setup>`) |
| Language | JavaScript ES Modules |
| Build tool | Vite |
| CSS framework | Bootstrap 5.3.x |
| Icons | Bootstrap Icons |
| Routing | Vue Router |
| State | Vue Reactivity (`ref`, `computed`) |
| Local persistence | LocalStorage (settings only) |
| Styling | Custom CSS (CSS variables) + Arabic.css |
| Unit testing | Vitest |
| Code quality | ESLint (flat config) + Prettier |

**Avoided:** jQuery, Tailwind, Vuex/Pinia, Axios, Lodash, backend, databases, auth, AI APIs.

---

## 3. Architecture

Client-side SPA. No backend. Quran content is static JSON separate from code. User settings stored in LocalStorage.

```
Browser
  |
  v
Vue App (App.vue + router-view)
  |
  +-- HomeView
  +-- SurahListView
  +-- LearningView
  +-- ResultsView (stub)
  +-- HistoryView (stub)
  +-- SettingsView (stub)
  |
  v
Composables
  +-- useQuran
  +-- useSettings
  |
  v
Services
  +-- quranService (load/validate/getVerse/getWord)
  +-- settingsService (load/save/apply font sizes)
  |
  v
Browser Storage / Static JSON
  +-- LocalStorage (settings)
  +-- public/data/surahs/surah-*.json
```

---

## 4. Routes (implemented in `src/router/index.js`)

| Path | Component | Status |
|---|---|---|
| `/` | HomeView | Implemented |
| `/surahs` | SurahListView | Implemented |
| `/surah/:id` | LearningView | Implemented |
| `/surah/:id/results` | ResultsView | Stub (`<h1>Results</h1>`) |
| `/history` | HistoryView | Stub (`<h1>History</h1>`) |

`SettingsView` exists but is not registered in the router; it is opened via offcanvas in `App.vue`.

---

## 5. Pages & Components

### 5.1 App.vue (`src/App.vue`)
App shell: Bootstrap navbar (Home, Surahs, History, Settings), `<router-view />`, settings offcanvas with Arabic/English font-size range inputs bound to `useSettings()`.

### 5.2 HomeView (`src/views/HomeView.vue`)
Welcome message + "Browse Surahs" button linking to `/surahs`.

### 5.3 SurahListView (`src/views/SurahListView.vue`)
Hardcoded single entry: Surah 1 Al-Fatiha (7 verses), "Open" button to `/surah/1`.

### 5.4 LearningView (`src/views/LearningView.vue`)
Loads a Surah via `useQuran()` and renders:
- Surah name (English / Arabic / transliteration)
- Each verse: number, Arabic text (RTL), individually segmented words with primary English meaning below each word, verse translation, verse explanation

Each of the three display lines is togglable from settings:
- Arabic verse line
- Word-by-word meanings line
- Verse translation line

Defaults: all three shown. Reading mode only. No test mode, no word-details panel yet.

### 5.5 ResultsView / HistoryView / SettingsView
Stubs. No functionality yet.

---

## 6. Composables

### 6.1 `useQuran` (`src/composables/useQuran.js`)
Exposes: `surah`, `verses`, `currentVerse`, `words`, `currentVerseId`, `loading`, `error`, `load(id)`, `setVerse(id)`.
- `load(id)` fetches and caches the Surah, sets current verse to the first.

### 6.2 `useSettings` (`src/composables/useSettings.js`)
Exposes: `arabicFontSize`, `englishFontSize`, `showArabicVerse`, `showWordMeanings`, `showTranslation`, `load()`, `apply()`.
- Loads/saves font sizes and display toggles via `settingsService`, applies font-size CSS custom properties on `:root`.

---

## 7. Services

### 7.1 `quranService` (`src/services/quranService.js`)
- `validateSurah(data)` — validates schema_version, content_version, surah, languages, verses, words, required fields, unique IDs, word positions, accepted answers. Throws on invalid.
- `loadSurah(id)` — loads `public/data/surahs/surah-{id}.json` (fetch in browser, node:fs in SSR), validates, caches in memory.
- `getVerse(surahId, verseId)` — returns verse by id or number.
- `getWord(surahId, verseId, wordId)` — returns word by id or position.
- `clearCache()` — clears the in-memory surah cache.

### 7.2 `settingsService` (`src/services/settingsService.js`)
- `loadSettings()` — reads Arabic/English font size and display toggles from LocalStorage with defaults.
- `saveSettings(partial)` — merges and persists settings to LocalStorage.
- `applySettings(settings)` — writes `--quran-font-size-arabic` / `--quran-font-size-english` CSS vars on `document.documentElement`.
- Display toggles: `showArabicVerse`, `showWordMeanings`, `showTranslation` (all default `true`).
- Exports `STORAGE_KEYS`, `DEFAULTS`, `CSS_VARS`, `MIN_FONT_SIZE`, `MAX_FONT_SIZE`.

---

## 8. Content JSON (`public/data/surahs/surah-001.json`)

One file per Surah. Implemented structure:

```json
{
  "schema_version": "1.0",
  "content_version": "1.0.0",
  "surah": { "id", "number", "name": {arabic, transliteration, english}, "revelation_type", "total_verses", "total_words" },
  "languages": { "en": { "name", "direction" } },
  "verses": [
    {
      "id", "number",
      "arabic": { "text" },
      "translation": { "en": { "text", "source": { "id" } } },
      "explanation": null | string,
      "words": [
        {
          "id", "position",
          "arabic", "transliteration",
          "meanings": { "en": { "primary", "alternatives": [], "accepted_answers": [] } },
          "root": null,
          "grammar": null,
          "explanation": null
        }
      ]
    }
  ],
  "sources": [ { "id", "name", "type", "url", "license" } ]
}
```

Surah 1 (Al-Fatiha): 7 verses, 29 words, all fields populated. Sources: Quran.com API v4, Sahih International.

---

## 9. Styling

- `src/assets/styles/custom.css` — `:root` CSS vars `--quran-font-size-arabic` (1.5rem), `--quran-font-size-english` (1rem); `.english-text` uses the English var.
- `src/assets/styles/arabic.css` — `.arabic` / `.arabic-text`: `direction: rtl`, `font-family: "Amiri", serif`, font-size from CSS var.
- `main.js` imports Bootstrap CSS/JS, Bootstrap Icons CSS, custom.css, arabic.css.

---

## 10. Storage

- **Settings:** LocalStorage keys `quran:settings:arabicFontSize`, `quran:settings:englishFontSize`, `quran:settings:showArabicVerse`, `quran:settings:showWordMeanings`, `quran:settings:showTranslation`.
- **Quran progress / test answers / history:** Not yet implemented.
- Storage is browser/device-specific; no sync.

---

## 11. Testing (`webapp/tests/`)

| Test file | Coverage |
|---|---|
| `quranData.test.js` | JSON structure, required fields, verse/word counts, unique IDs, word positions, accepted answers, sources |
| `quranService.test.js` | loadSurah + validation, caching, getVerse, getWord, validateSurah rejection |

No tests yet for settingsService, answer checking, scoring, or views.

---

## 12. Configuration

- `vite.config.js` — Vue plugin only.
- `eslint.config.js` — Flat config, `eslint-plugin-vue` essential, no custom rules.
- `package.json` scripts: `dev`, `build`, `preview`, `lint`, `format`, `test`.

---

## 13. Not Yet Implemented (planned, not in spec as done)

- Test mode (Reading/Test toggle, answer inputs)
- Answer checking service (`answerChecker.js`)
- Progress service (`progressService.js`) + LocalStorage progress
- Word details panel (click word → bottom sheet / side panel)
- Results page functionality (scoring, verse-level results, corrections)
- History page functionality
- Settings page functionality (route not registered)
- PWA / service worker / offline caching
- Ajv JSON validation (manual validation only in quranService)

---

## 14. Implementation Rules (spec-driven)

1. Check SPEC.md before changing code.
2. If a requirement is missing or changed, update SPEC.md first.
3. Write a failing test (red) in `webapp/tests/`.
4. Implement minimal code in `webapp/src/`.
5. Run tests (green), then lint (ESLint + Prettier).
6. Keep components small; business logic in services, not components.
7. Do not hardcode Quran content in components; JSON is source of truth.
8. Do not introduce backend, databases, auth, or AI answer checking.
9. Keep mobile-first design.
10. Project must build successfully at the end of each phase.
