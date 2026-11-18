import { describe, it, expect } from "vitest";
import data from "../public/data/surahs/surah-001.json";

describe("Quran data: Surah Al-Fatiha", () => {
  it("is valid JSON with required top-level fields", () => {
    expect(data).toBeTruthy();
    expect(data.schema_version).toBeTruthy();
    expect(data.content_version).toBeTruthy();
    expect(data.surah).toBeTruthy();
    expect(data.languages).toBeTruthy();
    expect(Array.isArray(data.verses)).toBe(true);
    expect(Array.isArray(data.sources)).toBe(true);
  });

  it("has surah info", () => {
    const s = data.surah;
    expect(s.id).toBe(1);
    expect(s.number).toBe(1);
    expect(s.name).toBeTruthy();
    expect(s.name.arabic).toBeTruthy();
    expect(s.name.transliteration).toBeTruthy();
    expect(s.name.english).toBeTruthy();
    expect(s.revelation_type).toBeTruthy();
    expect(typeof s.total_verses).toBe("number");
    expect(typeof s.total_words).toBe("number");
  });

  it("verse count equals total_verses", () => {
    expect(data.verses.length).toBe(data.surah.total_verses);
  });

  it("has unique verse ids", () => {
    const ids = data.verses.map((v) => v.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("verses have required fields", () => {
    for (const v of data.verses) {
      expect(v.id).toBeTruthy();
      expect(v.number).toBeTruthy();
      expect(v.arabic).toBeTruthy();
      expect(typeof v.arabic.text).toBe("string");
      expect(v.translation).toBeTruthy();
      expect(v.words).toBeTruthy();
      expect(Array.isArray(v.words)).toBe(true);
    }
  });

  it("translation language structure", () => {
    for (const v of data.verses) {
      expect(v.translation.en).toBeTruthy();
      expect(typeof v.translation.en.text).toBe("string");
      expect(v.translation.en.source).toBeTruthy();
    }
  });

  it("word ids are unique within a verse", () => {
    for (const v of data.verses) {
      const ids = v.words.map((w) => w.id);
      expect(new Set(ids).size).toBe(ids.length);
    }
  });

  it("word positions are valid", () => {
    for (const v of data.verses) {
      const positions = v.words.map((w) => w.position);
      positions.forEach((p, i) => expect(p).toBe(i + 1));
    }
  });

  it("words have required fields", () => {
    for (const v of data.verses) {
      for (const w of v.words) {
        expect(w.id).toBeTruthy();
        expect(typeof w.position).toBe("number");
        expect(typeof w.arabic).toBe("string");
        expect(w.meanings).toBeTruthy();
        expect(w.meanings.en).toBeTruthy();
        expect(typeof w.meanings.en.primary).toBe("string");
        expect(Array.isArray(w.meanings.en.alternatives)).toBe(true);
        expect(Array.isArray(w.meanings.en.accepted_answers)).toBe(true);
        expect(w.meanings.en.accepted_answers.length).toBeGreaterThan(0);
      }
    }
  });

  it("word count equals total_words", () => {
    const total = data.verses.reduce((sum, v) => sum + v.words.length, 0);
    expect(total).toBe(data.surah.total_words);
  });

  it("word id format", () => {
    for (const v of data.verses) {
      for (const w of v.words) {
        expect(w.id).toBe(`1:${v.number}:${w.position}`);
      }
    }
  });

  it("sources present", () => {
    expect(data.sources.length).toBeGreaterThan(0);
  });
});
