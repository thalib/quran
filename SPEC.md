# Quran Learning App
## Software Design & Implementation Specification

**Document Version:** 1.0  
**Project Type:** Client-side Single Page Application (SPA)  
**Target Platform:** Mobile, Tablet and Desktop  
**Initial Language:** English  
**Initial Content:** Surah Al-Fatiha  
**Development Approach:** AI-assisted, incremental implementation

---

# 1. Project Overview

## 1.1 Purpose

Build a lightweight, modern Quran learning application for people who do not understand Arabic.

The application helps users understand the Quran word by word through reading, explanations and self-assessment.

Users should be able to:

- Read Quranic Arabic with individual word segmentation.
- See the English meaning of each Arabic word.
- Read a complete English translation of each verse.
- Explore word roots, grammar and explanations.
- Test their understanding by entering English meanings.
- Receive automatic assessment and corrections.
- Track their learning progress.

The application should provide a clean reading experience rather than feeling like a traditional quiz application.

## 1.2 Core Product Principle

**Learn the Quran, one word at a time.**

The application must prioritize:

1. Quran content accuracy.
2. Simple user experience.
3. Mobile-first design.
4. Fast performance.
5. Offline functionality.
6. Maintainable architecture.
7. Future multilingual support.

## 1.3 Initial Scope

Version 1.0 will support:

- English interface.
- English word meanings.
- English verse translations.
- English explanations.
- Surah Al-Fatiha as initial learning content.
- Reading mode.
- Test mode.
- Assessment and results.
- Local progress tracking.
- Offline functionality.

The architecture must support all 114 Surahs and additional languages without requiring a major redesign.

---

# 2. Technology Stack

Use the following technology stack.

| Category | Technology | Purpose |
|---|---|---|
| Frontend framework | Vue 3 | Application UI |
| Language | JavaScript ES Modules | Application logic |
| Build tool | Vite | Development and production builds |
| CSS framework | Bootstrap 5.3.x | Responsive UI and styling |
| Icons | Bootstrap Icons | Application icons |
| Routing | Vue Router | SPA navigation |
| State management | Vue Reactivity | Shared application state |
| Local persistence | LocalStorage | User progress and settings |
| Offline support | PWA + Service Worker | Offline application |
| PWA integration | vite-plugin-pwa | Service worker generation |
| Unit testing | Vitest | Business logic tests |
| Code quality | ESLint + Prettier | Code consistency |
| JSON validation | Ajv | Content validation |

Use the latest stable compatible versions of these dependencies when creating the project.

Bootstrap 6 should only be considered after it becomes production-stable.

## 2.1 Technology Guidelines

- Use Vue 3 Composition API.
- Use Vue Single File Components.
- Use `<script setup>`.
- Use JavaScript, not TypeScript, initially.
- Use native `fetch()` for loading JSON.
- Use Vue Router for navigation.
- Use Vue's built-in `ref`, `reactive` and `computed` for state.
- Avoid adding Pinia unless shared state becomes difficult to manage.
- Use Bootstrap CSS and utility classes.
- Use custom CSS only where Bootstrap is insufficient.
- Use native browser APIs where practical.

## 2.2 Avoid Unnecessary Dependencies

Do not introduce:

- jQuery.
- Tailwind CSS.
- Vuex.
- Axios.
- Lodash.
- Large component libraries.
- Backend frameworks.
- Database servers.
- Authentication systems.
- AI APIs for answer checking.

Keep the application lightweight.

---

# 3. Application Architecture

The application is a fully client-side SPA.

There is no backend, server database or user authentication in Version 1.

## 3.1 High-Level Architecture

    User
      |
      v
    Vue Application
      |
      +-- Home
      |
      +-- Surah Selection
      |
      +-- Learning
      |     |
      |     +-- Reading Mode
      |     |
      |     +-- Test Mode
      |     |
      |     +-- Word Details
      |     |
      |     +-- Verse Details
      |
      +-- Results
      |
      +-- History
      |
      +-- Settings
      |
      v
    Application Services
      |
      +-- Quran Service
      +-- Answer Checker
      +-- Score Service
      +-- Progress Service
      +-- Settings Service
      |
      v
    Browser Storage
      |
      +-- LocalStorage
      |
      v
    Static JSON Content

## 3.2 Content Architecture

Quran content must be stored separately from application code.

Use JSON files, with one file per Surah.

Example:

    public/
      data/
        surahs/
          surah-001.json
          surah-002.json
          surah-003.json

The application loads the relevant Surah JSON when required.

Do not hardcode Quran content inside Vue components.

## 3.3 User Data Architecture

Keep user-specific information separate from Quran content.

Store:

- Test answers.
- Learning progress.
- Test history.
- User settings.
- Last visited Surah and verse.

Use LocalStorage initially.

The application must continue working without a backend.

---

# 4. Application Pages and Navigation

Use Vue Router.

Required routes:

| Route | Page |
|---|---|
| `/` | Home |
| `/surahs` | Surah selection |
| `/surah/:id` | Learning page |
| `/surah/:id/results` | Assessment results |
| `/history` | Learning history |
| `/settings` | Application settings |

Navigation must happen without full page reloads.

## 4.1 Home Page

Purpose: Give users a simple starting point.

Components:

- Welcome section.
- Continue learning card.
- Recently studied Surah.
- Basic progress summary.
- Browse Surahs button.

Display:

- Surahs started.
- Tests completed.
- Last studied Surah.
- Latest learning activity.

If the user has no progress, show a simple welcome message and a button to browse Surahs.

## 4.2 Surah Selection Page

Display available Surahs.

Each Surah item should show:

- Surah number.
- Arabic name.
- English name.
- Transliteration.
- Verse count.
- Learning progress.
- Availability status.

Initially, only Surah Al-Fatiha is enabled.

The data architecture must support all 114 Surahs.

## 4.3 Learning Page

This is the primary application page.

It must display the entire selected Surah on one scrollable page.

The user should be able to switch between Reading mode and Test mode.

Reading mode is the default.

---

# 5. Reading Mode

## 5.1 Purpose

Help users understand each verse and its individual words.

## 5.2 Verse Display

Each verse should contain:

1. Verse number.
2. Arabic verse.
3. Individually segmented Arabic words.
4. Primary English meaning under each word.
5. Complete English verse translation.
6. Verse-level explanation.

Example layout:

    Verse 1

    بِسْمِ        اللَّهِ        الرَّحْمَٰنِ
    In the name   Allah          The Most Merciful

    Translation:
    In the name of Allah, the Most Gracious,
    the Most Merciful.

    Explanation:
    Verse explanation goes here.

This is an illustrative layout, not verified Quran content.

## 5.3 Arabic Word Interaction

Each Arabic word must be individually clickable.

When a user clicks or taps a word, open its details.

Mobile:
- Use a bottom sheet.

Desktop:
- Use a side panel or popover.

The details panel should contain:

- Arabic word.
- Transliteration.
- Primary meaning.
- Alternative meanings.
- Root information, if available.
- Root meaning.
- Grammar and morphology, if available.
- Word-level explanation.

The user must be able to close the panel without losing their current reading position.

## 5.4 Reading Experience

- Arabic must render right-to-left.
- English must render left-to-right.
- Arabic font size must be independently adjustable.
- English font size must be independently adjustable.
- Arabic diacritics must render correctly.
- Quranic annotation marks must be supported.
- Maintain comfortable spacing between Arabic words.
- Use a verified, appropriately licensed Arabic font.
- Ensure the interface remains readable on small screens.

---

# 6. Test Mode

## 6.1 Purpose

Allow users to test their understanding of Arabic words.

## 6.2 Display Behavior

When the user switches to Test mode, hide:

- Primary word meanings.
- Alternative meanings.
- Root information.
- Grammar.
- Word explanations.
- Verse translations.
- Verse explanations.

Display:

- Arabic verse.
- Arabic words.
- English input field below each word.

Example:

    Verse 1

    بِسْمِ
    [ Enter meaning ]

    اللَّهِ
    [ Enter meaning ]

    الرَّحْمَٰنِ
    [ Enter meaning ]

## 6.3 Assessment Scope

Support two assessment scopes:

**Entire Surah**

Evaluate every word in the selected Surah.

**Individual Verse**

Evaluate only the words belonging to the selected verse.

## 6.4 Answer Input

Requirements:

- Each word has an independent input.
- Users can leave inputs empty.
- Answers should be saved automatically.
- Users can edit answers before submission.
- Inputs should be comfortable on mobile.
- Preserve answers when switching modes.
- Restore incomplete attempts after refreshing the browser.

## 6.5 Test Submission

Provide a clear Submit button.

Before submission, allow the user to review their answers.

On submission:

1. Collect answers.
2. Normalize answers.
3. Compare with accepted answers.
4. Calculate scores.
5. Store the completed attempt.
6. Navigate to the results page.

Do not silently submit when users switch modes.

---

# 7. Answer Checking and Scoring

Implement answer checking as a separate service.

File:

    src/services/answerChecker.js

## 7.1 Answer Normalization

Initially, use deterministic offline matching.

Normalization should:

- Convert text to lowercase.
- Trim leading and trailing spaces.
- Normalize repeated whitespace.
- Remove supported punctuation.
- Normalize Unicode consistently.

Do not implement fuzzy matching in Version 1.

Do not use an AI API for answer checking.

## 7.2 Accepted Answers

Each word must have predefined accepted answers in the Quran JSON.

Example:

    "accepted_answers": [
      "in the name",
      "by the name"
    ]

If the normalized user answer matches any accepted answer, mark it correct.

The primary meaning should be displayed as the suggested answer.

Do not automatically accept every alternative meaning. Accepted answers must be explicitly curated.

## 7.3 Answer Categories

Every submitted answer must be classified as one of:

- Correct.
- Incorrect.
- Unanswered.

## 7.4 Scoring Formula

Overall score:

    Correct Answers / Total Words * 100

Attempted accuracy:

    Correct Answers / (Correct Answers + Incorrect Answers) * 100

If no answers were attempted, attempted accuracy should be zero or shown as not applicable.

Round displayed percentages to whole numbers.

## 7.5 Result Information

Display:

- Total words.
- Attempted answers.
- Correct answers.
- Incorrect answers.
- Unanswered words.
- Overall score.
- Attempted accuracy.
- Verse-level scores.
- Word-level corrections.

Each incorrect or unanswered word should show:

- Arabic word.
- User answer.
- Primary meaning.
- Other accepted meanings, where useful.

Provide a button to return to Reading mode and review the words.

---

# 8. Quran Content JSON Specification

Use one JSON file per Surah.

Example:

    public/data/surahs/surah-001.json

## 8.1 Top-Level Structure

    {
      "schema_version": "1.0",
      "content_version": "1.0.0",

      "surah": {},

      "languages": {},

      "verses": [],

      "sources": []
    }

## 8.2 Surah Information

Fields:

- id
- number
- name
- revelation_type
- total_verses
- total_words

The Surah name should support:

- Arabic.
- Transliteration.
- English.

## 8.3 Verse Information

Each verse contains:

- id
- number
- arabic.text
- translation
- explanation
- words

Translation and explanation should support language codes.

Example:

    "translation": {
      "en": {
        "text": "English translation",
        "source": {
          "id": "translation-source-001"
        }
      }
    }

## 8.4 Word Information

Each word contains:

- id
- position
- arabic
- transliteration
- meanings
- root
- grammar
- explanation

Meanings must support:

    "meanings": {
      "en": {
        "primary": "Primary meaning",
        "alternatives": [],
        "accepted_answers": []
      }
    }

Root, grammar and explanations are optional.

Use null when the information is unavailable or not applicable.

## 8.5 Content Accuracy Requirements

- Quranic Arabic must come from a verified source.
- Word segmentation must be verified.
- Translations must be properly attributed.
- Root information must be verified.
- Grammar and morphology must be sourced.
- Explanations must have source references.
- Content licenses must be recorded.
- Do not invent missing linguistic information.

The JSON structure must be validated before content is included in production.

---

# 9. Local Storage and Progress

Create a separate progress service.

File:

    src/services/progressService.js

Use LocalStorage for Version 1.

## 9.1 Stored Information

For each Surah, save:

- Last visited date.
- Last visited verse.
- Total attempts.
- Best score.
- Latest score.
- Current incomplete answers.
- Completed test history.

Use a stable word identifier:

    surah_id:verse_id:word_id

Example:

    1:1:1
    1:1:2
    1:2:1

## 9.2 Auto-save

- Save answers when they change.
- Use a small debounce to avoid excessive writes.
- Restore saved answers when reopening an incomplete test.
- Save completed assessment results separately.
- Do not overwrite completed results when starting a new attempt.

## 9.3 Data Limitations

Progress is browser/device-specific.

There is no synchronization between devices.

If the user clears browser storage, progress may be lost.

Design the storage service so IndexedDB can be introduced later without changing the application components.

---

# 10. History Page

Show the user's learning activity.

For each Surah, display:

- Number of attempts.
- Latest score.
- Best score.
- Last practiced date.
- Completion status.

Allow users to open a previous result.

Keep the history interface simple.

---

# 11. Settings Page

Required settings:

| Setting | Default |
|---|---|
| Interface language | English |
| Meaning language | English |
| Arabic font size | Default |
| English font size | Default |
| Theme | Light |
| Auto-save | Enabled |

Provide a clear progress reset option with confirmation.

Keep interface language and Quran meaning language separate to support future multilingual functionality.

Use Bootstrap's color mode support for light and dark themes.

---

# 12. PWA and Offline Support

The application must be installable as a Progressive Web App.

Use vite-plugin-pwa.

## 12.1 Offline Requirements

Cache:

- Application shell.
- JavaScript.
- CSS.
- Fonts.
- Icons.
- Quran JSON files.

Keep all CSS and JS bundled locally; do not depend on CDN-hosted assets so the app works fully offline without network.

Once the application and required Surah content have been cached, users should be able to access them offline.

## 12.2 Service Worker

Implement:

- Application asset caching.
- Quran content caching.
- Offline fallback.
- Application update handling.

Use versioned content and sensible cache invalidation.

Do not allow a stale service worker to silently prevent users from receiving important application updates.

---

# 13. Project Directory Structure

Use the following top-level structure (all application code lives under `webapp/`).

    webapp/
    ├── public/
    ├── src/
    ├── tests/
    ├── scripts/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── README.md

Exact file names and nested layout can be read and understood from the codebase; preserve the general separation of responsibilities (assets, components, views, composables, services, router, etc.).

---

# 14. UI and UX Guidelines

## 14.1 General Design

The interface should be:

- Modern.
- Minimal.
- Clean.
- Mobile-first.
- Comfortable for extended reading.
- Consistent across all pages.

Avoid unnecessary animations, decorative elements and complex layouts.

## 14.2 Responsive Design

Support:

- Small mobile screens.
- Large mobile screens.
- Tablets.
- Desktop.

Use Bootstrap responsive grid and utility classes.

## 14.3 Arabic Display

Arabic content is central to the application.

Requirements:

- Correct RTL rendering.
- Proper Arabic font.
- Correct diacritics.
- Correct Quranic marks.
- Appropriate line height.
- Good word spacing.
- Independent font sizing.

Do not assume browser default fonts will render Quranic text consistently.

## 14.4 Accessibility

- Use semantic HTML.
- Provide labels for all inputs.
- Support keyboard navigation.
- Maintain sufficient color contrast.
- Provide visible focus indicators.
- Do not communicate correctness using color alone.
- Ensure touch targets are comfortable on mobile.

---

# 15. Testing Requirements

Use Vitest for unit testing.

## 15.1 Answer Checker Tests

Test:

- Exact correct answer.
- Accepted alternative answer.
- Incorrect answer.
- Empty answer.
- Case normalization.
- Leading and trailing spaces.
- Repeated whitespace.
- Supported punctuation.
- Unicode normalization.

## 15.2 Score Tests

Test:

- All answers correct.
- All answers incorrect.
- Some answers unanswered.
- Individual verse assessment.
- Entire Surah assessment.
- Zero attempted answers.

## 15.3 Progress Tests

Test:

- Save answers.
- Restore answers.
- Update scores.
- Save history.
- Clear progress.
- Restore incomplete attempts.

## 15.4 Quran Data Tests

Test:

- Valid JSON.
- Required fields.
- Unique verse IDs within a Surah.
- Unique word IDs within a verse.
- Valid word positions.
- Translation language structure.
- Accepted answer structure.
- Source references.
- Word counts.

---

# 16. Development Phases

Implement the application incrementally.

Do not attempt to build the entire application in one step.

## Phase 1: Project Foundation

Implement:

- Vue 3.
- Vite.
- Bootstrap.
- Bootstrap Icons.
- Vue Router.
- Global styles.
- Responsive application layout.
- Basic navigation.
- Home page.
- Surah selection page.

Deliverable: Running application with navigation and responsive layout.

## Phase 2: Quran Data Layer

Implement:

- JSON structure.
- JSON validation.
- Quran service.
- Surah loading.
- Verse loading.
- Word segmentation display.

Create initial Al-Fatiha data using verified content sources.

Deliverable: Al-Fatiha displayed with individually segmented Arabic words.

## Phase 3: Reading Mode

Implement:

- Reading mode interface.
- Word meanings.
- Complete verse translation.
- Verse explanation.
- Word details panel.
- Root and grammar display.
- Responsive Arabic typography.

Deliverable: Complete Al-Fatiha reading experience.

## Phase 4: Test Mode

Implement:

- Reading/Test mode switching.
- Word input fields.
- Entire Surah assessment.
- Individual verse assessment.
- Auto-save.
- Restore incomplete answers.

Deliverable: Functional self-assessment interface.

## Phase 5: Assessment Engine

Implement:

- Answer normalization.
- Accepted answer matching.
- Answer classification.
- Score calculation.
- Verse-level scoring.
- Word-level corrections.
- Results page.

Deliverable: Complete testing and results workflow.

## Phase 6: Progress and Settings

Implement:

- Local progress storage.
- Test history.
- Home page progress summary.
- Settings page.
- Light and dark themes.
- Adjustable font sizes.
- Clear progress functionality.

Deliverable: Complete local learning experience.

## Phase 7: PWA and Finalization

Implement:

- PWA manifest.
- Service worker.
- Offline caching.
- Application installation.
- Cache update strategy.
- Mobile testing.
- Accessibility checks.
- Production build.

Deliverable: Installable, offline-capable application.

---

# 17. Acceptance Criteria

Version 1.0 is considered complete when all the following requirements work.

## Application

- Application opens successfully.
- Navigation works without full page reloads.
- Layout works on mobile and desktop.
- Surah selection works.

## Quran Content

- Al-Fatiha displays all seven verses.
- Arabic words are individually segmented.
- Arabic text displays correctly.
- Verse translations display correctly.
- Word meanings display correctly.

## Reading Mode

- Reading mode is the default.
- Entire Surah is scrollable on one page.
- Tapping a word opens its details.
- Word details can be closed.
- Verse explanations are displayed.
- Arabic and English font sizes are independent.

## Test Mode

- Users can switch to Test mode.
- Learning information is hidden.
- Inputs appear below Arabic words.
- Users can test an entire Surah.
- Users can test an individual verse.
- Empty answers are allowed.
- Answers are automatically saved.
- Incomplete answers survive page refresh.

## Assessment

- Accepted alternative answers are recognized.
- Incorrect answers are identified.
- Empty answers are marked unanswered.
- Overall score is calculated correctly.
- Attempted accuracy is calculated correctly.
- Verse-level results are displayed.
- Word-level corrections are displayed.

## Progress

- Completed tests are saved.
- History is displayed.
- Best score is maintained.
- Latest score is maintained.
- Progress survives browser refresh.

## Offline

- Application can be installed.
- Previously cached content works offline.
- Reading and testing work offline.
- Progress can be saved offline.

---

# 18. Implementation Rules for the AI Coding Agent

These rules are mandatory throughout development.

1. Follow this document as the primary implementation specification.
2. Implement one development phase at a time.
3. Do not build all features in a single large implementation.
4. Keep components small and focused.
5. Keep business logic out of Vue components.
6. Put application logic in service files.
7. Do not hardcode Quran content in components.
8. Use JSON as the source of truth for Quran content.
9. Keep user progress separate from Quran content.
10. Do not introduce a backend.
11. Do not introduce unnecessary dependencies.
12. Do not use AI APIs for answer checking.
13. Do not invent Quranic text, meanings, roots, grammar or explanations.
14. Preserve mobile-first design.
15. Write unit tests for important business logic.
16. Validate Quran JSON before loading it.
17. Do not silently change the agreed architecture.
18. If a requirement is ambiguous, ask before making a significant architectural decision.
19. Keep the README updated with setup, development and build instructions.
20. Ensure the project builds successfully at the end of every phase.

## Definition of Done for Each Phase

Before moving to the next phase:

- All phase requirements are implemented.
- Application runs successfully.
- No critical console errors.
- Relevant tests pass.
- Mobile layout is checked.
- Existing functionality remains intact.
- README is updated where necessary.

If a feature is incomplete, report it clearly rather than marking the phase complete.

---

# 19. Deployment

The application should be deployable as a static website.

Possible hosting providers:

- Cloudflare Pages.
- Netlify.
- GitHub Pages.

No backend hosting is required.

The production build should contain the application assets and public Quran JSON files.

---

# 20. Final Architecture Decisions

The following decisions define Version 1.0.

| Area | Decision |
|---|---|
| Application type | Client-side SPA |
| Frontend | Vue 3 |
| Build tool | Vite |
| Language | JavaScript |
| CSS | Bootstrap 5.3.x |
| Icons | Bootstrap Icons |
| Navigation | Vue Router |
| State | Vue Reactivity |
| Quran content | Static JSON |
| JSON organization | One file per Surah |
| User storage | LocalStorage |
| Database | None |
| Backend | None |
| Authentication | None |
| Answer checking | Offline deterministic matching |
| Learning modes | Reading and Test |
| Default mode | Reading |
| Assessment scope | Verse or entire Surah |
| Languages | English initially |
| Offline | PWA |
| Initial content | Surah Al-Fatiha |

**The guiding principle: Build the simplest application that delivers an excellent Quran reading and learning experience. Avoid adding infrastructure or dependencies until they are genuinely needed.**
