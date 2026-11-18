const STORAGE_KEYS = {
  arabicFontSize: "quran:settings:arabicFontSize",
  englishFontSize: "quran:settings:englishFontSize",
  showArabicVerse: "quran:settings:showArabicVerse",
  showWordMeanings: "quran:settings:showWordMeanings",
  showTranslation: "quran:settings:showTranslation",
};

const DEFAULTS = {
  arabicFontSize: "1.5rem",
  englishFontSize: "1rem",
  showArabicVerse: true,
  showWordMeanings: true,
  showTranslation: true,
};

const CSS_VARS = {
  arabicFontSize: "--quran-font-size-arabic",
  englishFontSize: "--quran-font-size-english",
};

const TOGGLE_KEYS = ["showArabicVerse", "showWordMeanings", "showTranslation"];

const MIN_FONT_SIZE = 0.75;
const MAX_FONT_SIZE = 3;

function parseBoolean(raw, fallback) {
  if (raw === null || raw === undefined) return fallback;
  return String(raw).trim().toLowerCase() === "true";
}

function toNumber(value) {
  if (typeof value === "number") return value;
  if (typeof value === "string") {
    const match = value.trim().match(/^(-?\d*\.?\d+)/);
    if (match) return Number(match[1]);
  }
  return NaN;
}

function normalizeFontSize(value, fallback) {
  const fb = typeof fallback === "string" ? fallback : DEFAULTS.arabicFontSize;
  const num = toNumber(value);
  if (!Number.isFinite(num)) return fb;
  const clamped = Math.min(MAX_FONT_SIZE, Math.max(MIN_FONT_SIZE, num));
  return `${clamped}rem`;
}

function readStorage(key) {
  try {
    if (typeof localStorage === "undefined") return null;
    return localStorage.getItem(key);
  } catch (e) {
    return null;
  }
}

function writeStorage(key, value) {
  try {
    if (typeof localStorage !== "undefined") localStorage.setItem(key, value);
  } catch (e) {
    // ignore quota/blocked errors
  }
}

export function loadSettings() {
  const result = { ...DEFAULTS };
  for (const key of Object.keys(STORAGE_KEYS)) {
    const raw = readStorage(STORAGE_KEYS[key]);
    if (raw !== null) {
      if (TOGGLE_KEYS.includes(key)) {
        result[key] = parseBoolean(raw, DEFAULTS[key]);
      } else {
        result[key] = normalizeFontSize(raw, DEFAULTS[key]);
      }
    }
  }
  return result;
}

export function saveSettings(partial) {
  const current = loadSettings();
  const merged = { ...current };
  if (partial && typeof partial === "object") {
    for (const key of Object.keys(STORAGE_KEYS)) {
      if (Object.prototype.hasOwnProperty.call(partial, key)) {
        if (TOGGLE_KEYS.includes(key)) {
          const value = Boolean(partial[key]);
          merged[key] = value;
          writeStorage(STORAGE_KEYS[key], String(value));
        } else {
          const num = toNumber(partial[key]);
          if (!Number.isFinite(num)) continue;
          const normalized = normalizeFontSize(partial[key], DEFAULTS[key]);
          merged[key] = normalized;
          writeStorage(STORAGE_KEYS[key], normalized);
        }
      }
    }
  }
  return merged;
}

export function applySettings(settings) {
  const s = settings && typeof settings === "object" ? settings : {};
  const normalized = {
    arabicFontSize: normalizeFontSize(
      s.arabicFontSize !== undefined
        ? s.arabicFontSize
        : DEFAULTS.arabicFontSize,
      DEFAULTS.arabicFontSize,
    ),
    englishFontSize: normalizeFontSize(
      s.englishFontSize !== undefined
        ? s.englishFontSize
        : DEFAULTS.englishFontSize,
      DEFAULTS.englishFontSize,
    ),
  };
  try {
    if (typeof document !== "undefined" && document.documentElement) {
      document.documentElement.style.setProperty(
        CSS_VARS.arabicFontSize,
        normalized.arabicFontSize,
      );
      document.documentElement.style.setProperty(
        CSS_VARS.englishFontSize,
        normalized.englishFontSize,
      );
    }
  } catch (e) {
    // ignore
  }
  return normalized;
}

export { STORAGE_KEYS, DEFAULTS, CSS_VARS, MIN_FONT_SIZE, MAX_FONT_SIZE };
