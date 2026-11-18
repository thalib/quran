import { describe, it, expect, beforeEach, vi } from "vitest";

const localStorageMock = vi.hoisted(() => {
  const store = {};
  return {
    getItem: (key) => store[key] ?? null,
    setItem: (key, value) => {
      store[key] = String(value);
    },
    clear: () => {
      Object.keys(store).forEach((key) => delete store[key]);
    },
  };
});

vi.stubGlobal("localStorage", localStorageMock);

import {
  loadSettings,
  saveSettings,
  applySettings,
  DEFAULTS,
  STORAGE_KEYS,
} from "../src/services/settingsService.js";

function clearStorage() {
  localStorageMock.clear();
}

describe("settingsService: display toggles", () => {
  beforeEach(() => {
    clearStorage();
    vi.restoreAllMocks();
  });

  it("defaults all toggles to true", () => {
    const s = loadSettings();
    expect(s.showArabicVerse).toBe(true);
    expect(s.showWordMeanings).toBe(true);
    expect(s.showTranslation).toBe(true);
  });

  it("DEFAULTS has toggle keys", () => {
    expect(DEFAULTS.showArabicVerse).toBe(true);
    expect(DEFAULTS.showWordMeanings).toBe(true);
    expect(DEFAULTS.showTranslation).toBe(true);
  });

  it("STORAGE_KEYS has toggle keys", () => {
    expect(STORAGE_KEYS.showArabicVerse).toBe("quran:settings:showArabicVerse");
    expect(STORAGE_KEYS.showWordMeanings).toBe(
      "quran:settings:showWordMeanings",
    );
    expect(STORAGE_KEYS.showTranslation).toBe("quran:settings:showTranslation");
  });

  it("saves and loads toggle values", () => {
    const saved = saveSettings({
      showArabicVerse: false,
      showWordMeanings: true,
      showTranslation: false,
    });
    expect(saved.showArabicVerse).toBe(false);
    expect(saved.showWordMeanings).toBe(true);
    expect(saved.showTranslation).toBe(false);

    const loaded = loadSettings();
    expect(loaded.showArabicVerse).toBe(false);
    expect(loaded.showWordMeanings).toBe(true);
    expect(loaded.showTranslation).toBe(false);
  });

  it("persists toggles to localStorage", () => {
    saveSettings({ showArabicVerse: false });
    expect(localStorageMock.getItem("quran:settings:showArabicVerse")).toBe(
      "false",
    );
  });

  it("applySettings does not throw without document", () => {
    const origDoc = global.document;
    // @ts-expect-error testing no-document environment
    global.document = undefined;
    expect(() => applySettings({ showArabicVerse: false })).not.toThrow();
    global.document = origDoc;
  });
});
