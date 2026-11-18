import { describe, it, expect, beforeEach } from "vitest";
import {
  validateSurah,
  loadSurah,
  getVerse,
  getWord,
  clearCache,
} from "../src/services/quranService.js";

describe("quranService", () => {
  beforeEach(() => {
    clearCache();
  });

  it("loads surah 1 and validates", async () => {
    const s = await loadSurah(1);
    expect(s.surah.number).toBe(1);
    expect(s.verses.length).toBe(7);
  });

  it("returns cached instance on repeat load", async () => {
    const a = await loadSurah(1);
    const b = await loadSurah(1);
    expect(a).toBe(b);
  });

  it("getVerse returns verse by number", async () => {
    const v = await getVerse(1, 2);
    expect(v.number).toBe(2);
    expect(v.words.length).toBe(4);
  });

  it("getVerse throws for missing verse", async () => {
    await expect(getVerse(1, 99)).rejects.toThrow();
  });

  it("getWord returns word by id", async () => {
    const w = await getWord(1, 1, "1:1:1");
    expect(w.arabic).toBe("بِسْمِ");
    expect(w.position).toBe(1);
  });

  it("getWord throws for missing word", async () => {
    await expect(getWord(1, 1, "1:1:99")).rejects.toThrow();
  });

  it("validateSurah rejects invalid data", () => {
    expect(() => validateSurah(null)).toThrow();
    expect(() => validateSurah({})).toThrow();
    expect(() =>
      validateSurah({
        schema_version: "1.0",
        content_version: "1.0.0",
        surah: {
          id: 1,
          number: 1,
          name: { arabic: "a", transliteration: "b", english: "c" },
          total_verses: 1,
          total_words: 1,
        },
        languages: {},
        verses: [],
        sources: [{ id: "s" }],
      }),
    ).toThrow();
  });
});
