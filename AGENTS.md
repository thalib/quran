# Quran Learning App

## Directory Structure

All application code lives under `webapp/`. Use the framework-standard top-level layout only:

```
webapp/
├── public/        # static assets and Quran JSON data
├── src/           # application source code
│   ├── assets/    # styles and static assets
│   ├── components/# Vue components by feature
│   ├── views/     # route-level pages
│   ├── composables/# reusable composition functions
│   ├── services/  # business logic services
│   └── router/    # Vue Router config
├── tests/         # unit tests
├── scripts/       # build/validation scripts
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

Exact file names and nested layout can be read and understood from the codebase.

Spec: `SPEC.md` is the single source of truth for this app.

## Must Follow Rules

- Always use relative paths; never use absolute paths to access files unless explicitly instructed.
- For temporary work, use `temp/tmp/` instead of `/tmp`.
- Keep all CSS and JS bundled locally; do not depend on CDN-hosted assets so the app works fully offline without network.
- Always stop dev servers and background completions (build/test/watch processes) when finished; never leave them running.
  1. **Check spec** — read `SPEC.md` (single source of truth) and understand the requirement.
  2. **Update spec** — if the requirement changes or is missing, update the spec first.
  3. **Write failing test (red)** — add/update tests in `webapp/tests/` that encode the expected behavior; confirm they fail.
  4. **Implement/refactor code** — write the minimal code in `webapp/src/` to satisfy the tests.
  5. **Make test pass (green)** — run tests and ensure all pass.
  6. **Lint** — run ESLint + Prettier; fix all issues.
  7. **Summary** — report what changed, test results, and any caveats.
