const STORAGE_KEY = "quran:progress";

function readStorage(key) {
  try {
    if (typeof localStorage === "undefined") return null;
    return localStorage.getItem(key);
  } catch {
    return null;
  }
}

function writeStorage(key, value) {
  try {
    if (typeof localStorage !== "undefined") localStorage.setItem(key, value);
  } catch {
    // ignore
  }
}

function safeParse(raw) {
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function emptyProgress() {
  return { surahs: {} };
}

export function loadProgress() {
  const parsed = safeParse(readStorage(STORAGE_KEY));
  if (!parsed || typeof parsed !== "object") return emptyProgress();
  if (!parsed.surahs || typeof parsed.surahs !== "object") parsed.surahs = {};
  return parsed;
}

export function saveProgress(progress) {
  const p = progress && typeof progress === "object" ? progress : emptyProgress();
  if (!p.surahs || typeof p.surahs !== "object") p.surahs = {};
  writeStorage(STORAGE_KEY, JSON.stringify(p));
  return p;
}

function surahKey(id) {
  return String(id);
}

function ensureSurah(progress, surahId) {
  if (!progress.surahs) progress.surahs = {};
  const key = surahKey(surahId);
  if (!progress.surahs[key] || typeof progress.surahs[key] !== "object") {
    progress.surahs[key] = {
      surahId: Number.isFinite(Number(surahId)) ? Number(surahId) : surahId,
      lastVisitedDate: null,
      lastVisitedVerse: null,
      totalAttempts: 0,
      bestScore: 0,
      latestScore: 0,
      currentAnswers: {},
      history: [],
    };
  }
  return progress.surahs[key];
}

export function getSurahProgress(surahId) {
  const p = loadProgress();
  return p.surahs[surahKey(surahId)] || null;
}

export function updateLastVisited(surahId, verseId) {
  const p = loadProgress();
  const s = ensureSurah(p, surahId);
  s.lastVisitedDate = new Date().toISOString();
  if (verseId !== undefined) s.lastVisitedVerse = verseId;
  saveProgress(p);
  return s;
}

export function saveAnswers(surahId, answers) {
  const p = loadProgress();
  const s = ensureSurah(p, surahId);
  s.currentAnswers = answers && typeof answers === "object" ? { ...answers } : {};
  s.lastVisitedDate = new Date().toISOString();
  saveProgress(p);
  return s;
}

export function loadAnswers(surahId) {
  const s = getSurahProgress(surahId);
  return s && s.currentAnswers ? { ...s.currentAnswers } : {};
}

export function recordAttempt(surahId, result) {
  const p = loadProgress();
  const s = ensureSurah(p, surahId);
  const score =
    result && (result.overallScore ?? result.overall ?? result.score ?? result.percentage) != null
      ? Number(result.overallScore ?? result.overall ?? result.score ?? result.percentage)
      : 0;
  s.totalAttempts = (s.totalAttempts || 0) + 1;
  s.latestScore = score;
  s.bestScore = Math.max(s.bestScore || 0, score);
  s.lastVisitedDate = new Date().toISOString();
  if (!Array.isArray(s.history)) s.history = [];
  s.history.push({
    score,
    attemptedAt: new Date().toISOString(),
    ...(result || {}),
  });
  // clear current answers after completed attempt
  s.currentAnswers = {};
  saveProgress(p);
  return s;
}

export function saveAttempt(surahId, result) {
  return recordAttempt(surahId, result);
}

export function addHistory(surahId, result) {
  return recordAttempt(surahId, result);
}

export function getHistory() {
  const p = loadProgress();
  const out = [];
  for (const key of Object.keys(p.surahs || {})) {
    const s = p.surahs[key];
    out.push({
      surahId: s.surahId ?? Number(key),
      attempts: s.totalAttempts || 0,
      totalAttempts: s.totalAttempts || 0,
      latestScore: s.latestScore || 0,
      bestScore: s.bestScore || 0,
      lastVisitedDate: s.lastVisitedDate,
      lastPracticed: s.lastVisitedDate,
      history: Array.isArray(s.history) ? s.history : [],
    });
  }
  return out;
}

export function clearProgress() {
  try {
    if (typeof localStorage !== "undefined") localStorage.removeItem(STORAGE_KEY);
  } catch {
    // ignore
  }
  return emptyProgress();
}

export function resetProgress() {
  return clearProgress();
}

export function clearAllProgress() {
  return clearProgress();
}

// aliases
export const getProgress = loadProgress;
export const progress = loadProgress;
