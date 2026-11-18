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
const theme = ref(initial.theme);
const autoSave = ref(initial.autoSave);
const interfaceLanguage = ref(initial.interfaceLanguage);
const meaningLanguage = ref(initial.meaningLanguage);

applySettings(initial);

export function useSettings() {
  function load() {
    const s = loadSettings();
    arabicFontSize.value = s.arabicFontSize;
    englishFontSize.value = s.englishFontSize;
    showArabicVerse.value = s.showArabicVerse;
    showWordMeanings.value = s.showWordMeanings;
    showTranslation.value = s.showTranslation;
    theme.value = s.theme;
    autoSave.value = s.autoSave;
    interfaceLanguage.value = s.interfaceLanguage;
    meaningLanguage.value = s.meaningLanguage;
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
      theme: theme.value,
      autoSave: autoSave.value,
      interfaceLanguage: interfaceLanguage.value,
      meaningLanguage: meaningLanguage.value,
    });
    arabicFontSize.value = merged.arabicFontSize;
    englishFontSize.value = merged.englishFontSize;
    showArabicVerse.value = merged.showArabicVerse;
    showWordMeanings.value = merged.showWordMeanings;
    showTranslation.value = merged.showTranslation;
    theme.value = merged.theme;
    autoSave.value = merged.autoSave;
    interfaceLanguage.value = merged.interfaceLanguage;
    meaningLanguage.value = merged.meaningLanguage;
    applySettings(merged);
    return merged;
  }

  return {
    arabicFontSize,
    englishFontSize,
    showArabicVerse,
    showWordMeanings,
    showTranslation,
    theme,
    autoSave,
    interfaceLanguage,
    meaningLanguage,
    load,
    apply,
  };
}
