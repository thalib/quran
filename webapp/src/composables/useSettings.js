import { ref } from "vue";
import {
  loadSettings,
  saveSettings,
  applySettings,
} from "../services/settingsService.js";

const initial = loadSettings();

const arabicFontSize = ref(initial.arabicFontSize);
const englishFontSize = ref(initial.englishFontSize);
const showArabicVerse = ref(initial.showArabicVerse);
const showWordMeanings = ref(initial.showWordMeanings);
const showTranslation = ref(initial.showTranslation);

applySettings(initial);

export function useSettings() {
  function load() {
    const s = loadSettings();
    arabicFontSize.value = s.arabicFontSize;
    englishFontSize.value = s.englishFontSize;
    showArabicVerse.value = s.showArabicVerse;
    showWordMeanings.value = s.showWordMeanings;
    showTranslation.value = s.showTranslation;
    applySettings(s);
    return s;
  }

  function apply() {
    const merged = saveSettings({
      arabicFontSize: arabicFontSize.value,
      englishFontSize: englishFontSize.value,
      showArabicVerse: showArabicVerse.value,
      showWordMeanings: showWordMeanings.value,
      showTranslation: showTranslation.value,
    });
    arabicFontSize.value = merged.arabicFontSize;
    englishFontSize.value = merged.englishFontSize;
    showArabicVerse.value = merged.showArabicVerse;
    showWordMeanings.value = merged.showWordMeanings;
    showTranslation.value = merged.showTranslation;
    applySettings(merged);
    return merged;
  }

  return {
    arabicFontSize,
    englishFontSize,
    showArabicVerse,
    showWordMeanings,
    showTranslation,
    load,
    apply,
  };
}
