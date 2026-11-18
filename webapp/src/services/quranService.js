const cache = new Map();

function padId(id) {
  return String(id).padStart(3, "0");
}

function isObject(v) {
  return v !== null && typeof v === "object" && !Array.isArray(v);
}

export function validateSurah(data) {
  if (!isObject(data)) throw new Error("Surah data must be an object");
  if (typeof data.schema_version !== "string")
    throw new Error("Missing schema_version");
  if (typeof data.content_version !== "string")
    throw new Error("Missing content_version");
  if (!isObject(data.surah)) throw new Error("Missing surah");
  const s = data.surah;
  if (typeof s.id !== "number" || typeof s.number !== "number")
    throw new Error("Invalid surah id/number");
  if (
    !isObject(s.name) ||
    !s.name.arabic ||
    !s.name.transliteration ||
    !s.name.english
  )
    throw new Error("Invalid surah name");
  if (typeof s.total_verses !== "number" || typeof s.total_words !== "number")
    throw new Error("Invalid totals");
  if (!isObject(data.languages)) throw new Error("Missing languages");
  if (!Array.isArray(data.verses)) throw new Error("Missing verses");
  if (!Array.isArray(data.sources) || data.sources.length === 0)
    throw new Error("Missing sources");
  if (data.verses.length !== s.total_verses)
    throw new Error("Verse count mismatch");

  const verseIds = data.verses.map((v) => v.id);
  if (new Set(verseIds).size !== verseIds.length)
    throw new Error("Duplicate verse ids");

  let wordCount = 0;
  for (const v of data.verses) {
    if (typeof v.id !== "number" || typeof v.number !== "number")
      throw new Error("Invalid verse id/number");
    if (!isObject(v.arabic) || typeof v.arabic.text !== "string")
      throw new Error("Invalid verse arabic");
    if (!isObject(v.translation) || !isObject(v.translation.en))
      throw new Error("Invalid translation");
    if (typeof v.translation.en.text !== "string")
      throw new Error("Invalid translation text");
    if (!Array.isArray(v.words)) throw new Error("Invalid words");
    const ids = v.words.map((w) => w.id);
    if (new Set(ids).size !== ids.length) throw new Error("Duplicate word ids");
    v.words.forEach((w, i) => {
      if (w.position !== i + 1) throw new Error("Invalid word position");
      if (!isObject(w.meanings) || !isObject(w.meanings.en))
        throw new Error("Invalid meanings");
      if (typeof w.meanings.en.primary !== "string")
        throw new Error("Invalid primary meaning");
      if (!Array.isArray(w.meanings.en.alternatives))
        throw new Error("Invalid alternatives");
      if (
        !Array.isArray(w.meanings.en.accepted_answers) ||
        w.meanings.en.accepted_answers.length === 0
      )
        throw new Error("Missing accepted answers");
    });
    wordCount += v.words.length;
  }
  if (wordCount !== s.total_words) throw new Error("Word count mismatch");
  return data;
}

export async function loadSurah(id) {
  const key = String(id);
  if (cache.has(key)) return cache.get(key);
  let data;
  if (typeof window === "undefined") {
    const fs = await import(/* @vite-ignore */ "node:fs/promises");
    const nodePath = await import(/* @vite-ignore */ "node:path");
    const filePath = nodePath.resolve(
      process.cwd(),
      "public",
      "data",
      "surahs",
      `surah-${padId(id)}.json`,
    );
    const raw = await fs.readFile(filePath, "utf-8");
    data = JSON.parse(raw);
  } else {
    const url = `/data/surahs/surah-${padId(id)}.json`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Failed to load surah ${id}: ${res.status}`);
    data = await res.json();
  }
  const validated = validateSurah(data);
  cache.set(key, validated);
  return validated;
}

export async function getVerse(surahId, verseId) {
  const surah = await loadSurah(surahId);
  const verse = surah.verses.find(
    (v) => v.id === verseId || v.number === verseId,
  );
  if (!verse) throw new Error(`Verse ${verseId} not found in surah ${surahId}`);
  return verse;
}

export async function getWord(surahId, verseId, wordId) {
  const verse = await getVerse(surahId, verseId);
  const word = verse.words.find(
    (w) => w.id === wordId || w.position === wordId,
  );
  if (!word) throw new Error(`Word ${wordId} not found`);
  return word;
}

export function clearCache() {
  cache.clear();
}
